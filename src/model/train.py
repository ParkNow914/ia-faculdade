"""
SCRIPT DE TREINAMENTO DO MODELO LSTM
Pipeline completo de geração de dados, preprocessamento e treinamento.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Adicionar path do projeto
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.model.preprocessing import EnergyDataPreprocessor
from src.model.model import create_default_model


def plot_training_history(history, save_path='src/model/saved_models/training_history.png'):
    """
    Plota o histórico de treinamento.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Loss
    axes[0, 0].plot(history.history['loss'], label='Train Loss')
    axes[0, 0].plot(history.history['val_loss'], label='Val Loss')
    axes[0, 0].set_title('Model Loss (MSE)')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # MAE
    axes[0, 1].plot(history.history['mae'], label='Train MAE')
    axes[0, 1].plot(history.history['val_mae'], label='Val MAE')
    axes[0, 1].set_title('Mean Absolute Error')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('MAE')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # MAPE
    axes[1, 0].plot(history.history['mape'], label='Train MAPE')
    axes[1, 0].plot(history.history['val_mape'], label='Val MAPE')
    axes[1, 0].set_title('Mean Absolute Percentage Error')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('MAPE (%)')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Learning Rate (se disponível)
    axes[1, 1].text(0.5, 0.5, f'Total Epochs: {len(history.history["loss"])}', 
                    ha='center', va='center', fontsize=14)
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 Gráfico de treinamento salvo em: {save_path}")


def plot_predictions(y_true, y_pred, save_path='src/model/saved_models/predictions.png'):
    """
    Plota predições vs valores reais.
    """
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    # Plot 1: Time series (primeiras 200 amostras)
    n_samples = min(200, len(y_true))
    axes[0].plot(y_true[:n_samples], label='Real', alpha=0.7, linewidth=2)
    axes[0].plot(y_pred[:n_samples], label='Predito', alpha=0.7, linewidth=2)
    axes[0].set_title('Previsão vs Real (Primeiras 200 horas)')
    axes[0].set_xlabel('Hora')
    axes[0].set_ylabel('Consumo (kWh)')
    axes[0].legend()
    axes[0].grid(True)
    
    # Plot 2: Scatter plot
    axes[1].scatter(y_true, y_pred, alpha=0.5, s=10)
    axes[1].plot([y_true.min(), y_true.max()], 
                 [y_true.min(), y_true.max()], 
                 'r--', linewidth=2, label='Linha Ideal')
    axes[1].set_title('Predições vs Valores Reais')
    axes[1].set_xlabel('Valor Real (kWh)')
    axes[1].set_ylabel('Valor Predito (kWh)')
    axes[1].legend()
    axes[1].grid(True)
    
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
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'MAPE': mape
    }


def main():
    """
    Pipeline completo de treinamento.
    """
    print("="*80)
    print("🚀 MANUS-PREDICTOR - TREINAMENTO DO MODELO LSTM")
    print("="*80)
    
    # === PASSO 1: GERAR DATASET ===
    print("\n📊 PASSO 1: Verificando dataset...")
    
    if not os.path.exists('data/raw/energy_consumption.csv'):
        print("❌ Dataset não encontrado! Execute: python data/generate_dataset.py")
        return
    else:
        print("✅ Dataset já existe!")
    
    # === PASSO 2: PREPROCESSAMENTO ===
    print("\n🔧 PASSO 2: Preprocessando dados...")
    preprocessor = EnergyDataPreprocessor(sequence_length=24)
    
    df = preprocessor.load_data('data/raw/energy_consumption.csv')
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    
    # Salvar preprocessador
    preprocessor.save_scalers()
    
    # === PASSO 3: CRIAR MODELO ===
    print("\n🏗️ PASSO 3: Criando modelo LSTM...")
    model = create_default_model(
        sequence_length=24,
        n_features=X_train.shape[2]
    )
    
    # === PASSO 4: TREINAMENTO ===
    print("\n🎯 PASSO 4: Treinando modelo...")
    history = model.train(
        X_train, y_train,
        X_test, y_test,
        epochs=50,  # Reduzido para demonstração (use 100+ em produção)
        batch_size=64,
        verbose=1
    )
    
    # === PASSO 5: AVALIAÇÃO ===
    print("\n📊 PASSO 5: Avaliando modelo...")
    test_results = model.evaluate(X_test, y_test)
    
    # Fazer predições
    print("\n🔮 Gerando predições no conjunto de teste...")
    y_pred_scaled = model.predict(X_test)
    
    # Desnormalizar
    y_pred = preprocessor.inverse_transform_target(y_pred_scaled)
    y_true = preprocessor.inverse_transform_target(y_test)
    
    # Calcular métricas
    metrics = calculate_metrics(y_true, y_pred)
    
    print("\n" + "="*80)
    print("📈 RESULTADOS FINAIS")
    print("="*80)
    for metric, value in metrics.items():
        print(f"  {metric:10s}: {value:,.2f}")
    print("="*80)
    
    # === PASSO 6: VISUALIZAÇÕES ===
    print("\n📊 PASSO 6: Gerando visualizações...")
    os.makedirs('src/model/saved_models', exist_ok=True)
    
    plot_training_history(history)
    plot_predictions(y_true, y_pred)
    
    # === PASSO 7: SALVAR MODELO ===
    print("\n💾 PASSO 7: Salvando modelo final...")
    model.save_model('src/model/saved_models/lstm_model.h5')
    
    # Salvar configuração
    import json
    config = {
        'model_architecture': model.get_architecture_config(),
        'training_params': {
            'epochs': len(history.history['loss']),
            'final_loss': float(history.history['loss'][-1]),
            'final_val_loss': float(history.history['val_loss'][-1])
        },
        'metrics': {k: float(v) for k, v in metrics.items()}
    }
    
    with open('src/model/saved_models/model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*80)
    print("✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print("\n📁 Arquivos gerados:")
    print("  • src/model/saved_models/lstm_model.h5")
    print("  • src/model/saved_models/best_model.h5")
    print("  • src/model/saved_models/scaler_features.pkl")
    print("  • src/model/saved_models/scaler_target.pkl")
    print("  • src/model/saved_models/model_config.json")
    print("  • src/model/saved_models/training_history.png")
    print("  • src/model/saved_models/predictions.png")
    print("\n🚀 Próximo passo: Execute o backend com 'python src/backend/main.py'")
    

if __name__ == "__main__":
    main()
