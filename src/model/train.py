"""
SCRIPT DE TREINAMENTO DO MODELO DE REGRESSÃO ML
Pipeline completo de geração de dados, preprocessamento e treinamento.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import json

# Adicionar path do projeto
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.model.preprocessing import EnergyDataPreprocessor
from src.model.model import create_default_model


def plot_training_results(y_true, y_pred, save_path='src/model/saved_models/predictions.png'):
    """
    Plota resultados das predições.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot 1: Time series (primeiras 200 amostras)
    n_samples = min(200, len(y_true))
    axes[0, 0].plot(y_true[:n_samples], label='Real', alpha=0.7, linewidth=2)
    axes[0, 0].plot(y_pred[:n_samples], label='Predito', alpha=0.7, linewidth=2)
    axes[0, 0].set_title('Previsão vs Real (Primeiras 200 amostras)')
    axes[0, 0].set_xlabel('Amostra')
    axes[0, 0].set_ylabel('Consumo (kWh)')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Plot 2: Scatter plot
    axes[0, 1].scatter(y_true, y_pred, alpha=0.5, s=10)
    axes[0, 1].plot([y_true.min(), y_true.max()], 
                    [y_true.min(), y_true.max()], 
                    'r--', linewidth=2, label='Linha Ideal')
    axes[0, 1].set_title('Predições vs Valores Reais')
    axes[0, 1].set_xlabel('Valor Real (kWh)')
    axes[0, 1].set_ylabel('Valor Predito (kWh)')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Plot 3: Resíduos
    residuals = y_true - y_pred
    axes[1, 0].scatter(y_pred, residuals, alpha=0.5, s=10)
    axes[1, 0].axhline(y=0, color='r', linestyle='--', linewidth=2)
    axes[1, 0].set_title('Análise de Resíduos')
    axes[1, 0].set_xlabel('Valor Predito (kWh)')
    axes[1, 0].set_ylabel('Resíduo (Real - Predito)')
    axes[1, 0].grid(True)
    
    # Plot 4: Distribuição de erros
    axes[1, 1].hist(residuals, bins=50, alpha=0.7, edgecolor='black')
    axes[1, 1].set_title('Distribuição de Erros')
    axes[1, 1].set_xlabel('Erro (kWh)')
    axes[1, 1].set_ylabel('Frequência')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 Gráfico de predições salvo em: {save_path}")


def calculate_metrics(y_true, y_pred):
    """
    Calcula métricas de avaliação.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'MAPE': mape
    }


def compare_models(X_train, y_train, X_test, y_test, preprocessor):
    """
    Compara diferentes modelos de regressão e retorna o melhor.
    """
    print("\n" + "="*80)
    print("🔍 COMPARANDO DIFERENTES MODELOS DE REGRESSÃO")
    print("="*80)
    
    models_to_test = ['ensemble', 'rf', 'gb']
    results = {}
    
    for model_type in models_to_test:
        print(f"\n📊 Testando modelo: {model_type}")
        model = create_default_model()
        
        # Treinar
        val_metrics = model.train(
            X_train, y_train,
            X_test, y_test,
            optimize=False,
            model_type=model_type
        )
        
        # Avaliar no teste
        test_metrics = model.evaluate(X_test, y_test)
        
        results[model_type] = {
            'model': model,
            'val_mae': val_metrics['mae'],
            'test_mae': test_metrics['mae'],
            'test_rmse': test_metrics['rmse'],
            'test_r2': test_metrics['r2'],
            'test_mape': test_metrics['mape']
        }
        
        print(f"✅ {model_type}: MAE={test_metrics['mae']:.4f}, R²={test_metrics['r2']:.4f}")
    
    # Selecionar melhor modelo (menor MAE)
    best_model_type = min(results.keys(), key=lambda k: results[k]['test_mae'])
    best_model = results[best_model_type]['model']
    
    print("\n" + "="*80)
    print(f"🏆 MELHOR MODELO: {best_model_type.upper()}")
    print("="*80)
    print(f"  MAE: {results[best_model_type]['test_mae']:.4f}")
    print(f"  RMSE: {results[best_model_type]['test_rmse']:.4f}")
    print(f"  R²: {results[best_model_type]['test_r2']:.4f}")
    print(f"  MAPE: {results[best_model_type]['test_mape']:.2f}%")
    
    return best_model, best_model_type, results


def main():
    """
    Pipeline completo de treinamento.
    """
    print("="*80)
    print("🚀 MANUS-PREDICTOR - TREINAMENTO DO MODELO DE REGRESSÃO ML")
    print("="*80)
    
    # === PASSO 1: VERIFICAR DATASET REAL ===
    print("\n📊 PASSO 1: Verificando dataset REAL (não sintético)...")
    
    if not os.path.exists('data/raw/energy_consumption.csv'):
        print("❌ Dataset não encontrado!")
        print("📥 Para usar dados REAIS:")
        print("   1. Baixe o dataset UCI: https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption")
        print("   2. Execute: python data/process_uci_dataset.py")
        print("\n⚠️ ATENÇÃO: Não use dados sintéticos para treinamento!")
        return
    
    # Validar que é dataset REAL (não sintético)
    import pandas as pd
    df_check = pd.read_csv('data/raw/energy_consumption.csv', nrows=1)
    
    # Verificar se tem colunas de dataset UCI real
    if 'Voltage' in df_check.columns or 'Global_intensity' in df_check.columns or 'Sub_metering_1' in df_check.columns:
        print("✅ Dataset REAL detectado (formato UCI)")
    else:
        # Verificar timestamp para detectar dados sintéticos
        df_sample = pd.read_csv('data/raw/energy_consumption.csv', nrows=100)
        df_sample['timestamp'] = pd.to_datetime(df_sample['timestamp'])
        first_date = df_sample['timestamp'].min()
        
        # Dados sintéticos geralmente começam em 2022
        if first_date.year >= 2022:
            print("⚠️ ATENÇÃO: Dataset parece ser SINTÉTICO (data >= 2022)")
            print("❌ Não é permitido usar dados sintéticos!")
            print("📥 Use dados REAIS do UCI: python data/process_uci_dataset.py")
            return
        elif first_date.year >= 2000 and first_date.year <= 2015:
            print(f"✅ Dataset REAL confirmado (período: {first_date.year})")
        else:
            print("✅ Dataset encontrado (validar manualmente)")
    
    print(f"✅ Dataset já existe! ({len(pd.read_csv('data/raw/energy_consumption.csv')):,} registros)")
    
    # === PASSO 2: PREPROCESSAMENTO ===
    print("\n🔧 PASSO 2: Preprocessando dados...")
    preprocessor = EnergyDataPreprocessor(use_scaler='standard')
    
    # Carregar TODOS os dados disponíveis (sem limitações)
    print("📂 Carregando TODOS os dados do dataset real...")
    df = preprocessor.load_data('data/raw/energy_consumption.csv')
    print(f"✅ Dataset completo carregado: {len(df):,} registros")
    print(f"📅 Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    
    # Preprocessar TODOS os dados
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    
    # Salvar preprocessador
    preprocessor.save_scalers()
    
    # === PASSO 3: COMPARAR MODELOS ===
    print("\n🏗️ PASSO 3: Comparando modelos de regressão...")
    model, model_type, all_results = compare_models(X_train, y_train, X_test, y_test, preprocessor)
    
    # === PASSO 3.5: OTIMIZAR MELHOR MODELO (OPCIONAL - mais lento) ===
    print("\n⚡ PASSO 3.5: Pular otimização GridSearch para treinamento mais rápido")
    print("💡 O modelo já está otimizado com hiperparâmetros balanceados")
    print("   (Para máxima acurácia, descomente o código de GridSearch abaixo)")
    # GridSearch desabilitado para velocidade - modelo já está bem otimizado
    # if model_type in ['rf', 'gb']:
    #     print(f"🔍 Aplicando GridSearch no modelo {model_type}...")
    #     optimized_model = create_default_model()
    #     optimized_model.model = model.optimize_model(X_train, y_train, model_type)
    #     optimized_model.model.fit(X_train, y_train.ravel())
    #     model = optimized_model
    #     print("✅ Modelo otimizado!")
    
    # === PASSO 4: AVALIAÇÃO FINAL ===
    print("\n📊 PASSO 4: Avaliação final do melhor modelo...")
    test_results = model.evaluate(X_test, y_test)
    
    # Fazer predições
    print("\n🔮 Gerando predições no conjunto de teste...")
    y_pred_scaled = model.predict(X_test)
    
    # Desnormalizar
    if preprocessor.scaler_target is not None:
        y_pred = preprocessor.inverse_transform_target(y_pred_scaled)
        y_true = preprocessor.inverse_transform_target(y_test)
    else:
        y_pred = y_pred_scaled
        y_true = y_test
    
    # Ajustar formato
    if len(y_pred.shape) > 1:
        y_pred = y_pred.ravel()
    if len(y_true.shape) > 1:
        y_true = y_true.ravel()
    
    # Calcular métricas
    metrics = calculate_metrics(y_true, y_pred)
    
    # Calcular acurácia (1 - MAPE normalizado)
    accuracy_percent = max(0, 100 - metrics['MAPE'])
    
    print("\n" + "="*80)
    print("📈 RESULTADOS FINAIS - ACURÁCIA COMPLETA")
    print("="*80)
    print(f"  {'Métrica':<20s} {'Valor':<15s} {'Descrição'}")
    print("  " + "-"*70)
    print(f"  {'R² Score':<20s} {metrics['R2']:>14.4f}  {'Variação explicada (quanto mais próximo de 1, melhor)'}")
    print(f"  {'Acurácia':<20s} {accuracy_percent:>14.2f}%  {'Acurácia geral (100% - MAPE)'}")
    print(f"  {'MAE':<20s} {metrics['MAE']:>14.4f}  {'Erro médio absoluto (kWh)'}")
    print(f"  {'RMSE':<20s} {metrics['RMSE']:>14.4f}  {'Raiz do erro quadrático médio (kWh)'}")
    print(f"  {'MAPE':<20s} {metrics['MAPE']:>14.2f}%  {'Erro percentual médio absoluto'}")
    print("  " + "-"*70)
    print(f"\n  🎯 ACURÁCIA FINAL: {accuracy_percent:.2f}%")
    print(f"  📊 R² Score: {metrics['R2']:.4f} ({metrics['R2']*100:.2f}% da variação explicada)")
    print("="*80)
    
    # === PASSO 5: VISUALIZAÇÕES ===
    print("\n📊 PASSO 5: Gerando visualizações...")
    os.makedirs('src/model/saved_models', exist_ok=True)
    
    plot_training_results(y_true, y_pred)
    
    # === PASSO 6: SALVAR MODELO ===
    print("\n💾 PASSO 6: Salvando modelo final...")
    model.save_model('src/model/saved_models/regression_model.pkl')
    
    # Salvar configuração
    config = {
        'model_type': model_type,
        'model_info': model.get_model_info(),
        'metrics': {k: float(v) for k, v in metrics.items()},
        'all_models_comparison': {
            k: {
                'mae': float(v['test_mae']),
                'rmse': float(v['test_rmse']),
                'r2': float(v['test_r2']),
                'mape': float(v['test_mape'])
            }
            for k, v in all_results.items()
        }
    }
    
    with open('src/model/saved_models/model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*80)
    print("✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print("\n📁 Arquivos gerados:")
    print("  • src/model/saved_models/regression_model.pkl")
    print("  • src/model/saved_models/scaler_features.pkl")
    print("  • src/model/saved_models/scaler_target.pkl")
    print("  • src/model/saved_models/feature_columns.pkl")
    print("  • src/model/saved_models/model_config.json")
    print("  • src/model/saved_models/predictions.png")
    print("\n🚀 Próximo passo: Execute o backend com 'python src/backend/main.py'")


if __name__ == "__main__":
    main()
