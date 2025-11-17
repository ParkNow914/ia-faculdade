"""
ARQUITETURA DO MODELO DE REGRESSÃO ML PARA PREVISÃO DE ENERGIA
Usa algoritmos de Machine Learning tradicionais para previsão de consumo.
"""

import numpy as np
import joblib
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    VotingRegressor,
    StackingRegressor
)
from sklearn.linear_model import Ridge, Lasso
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Tentar importar XGBoost (opcional)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    import sys
    if sys.stdout.encoding and 'utf' not in sys.stdout.encoding.lower():
        print("[WARNING] XGBoost nao disponivel. Usando apenas scikit-learn.")
    else:
        print("⚠️ XGBoost não disponível. Usando apenas scikit-learn.")


class EnergyRegressionModel:
    """
    Modelo de regressão ML para previsão de consumo de energia elétrica.
    Usa ensemble de múltiplos algoritmos para máxima acurácia.
    """
    
    def __init__(self):
        """Inicializa o modelo de regressão."""
        self.model = None
        self.best_model = None
        self.best_score = None
        self.model_name = None
        
    def create_base_models(self):
        """
        Cria modelos base para ensemble.
        
        Returns:
            Lista de tuplas (nome, modelo)
        """
        models = [
            ('rf', RandomForestRegressor(
                n_estimators=300,  # Aumentado para melhor acurácia (ainda rápido)
                max_depth=30,      # Profundidade máxima para capturar padrões complexos
                min_samples_split=2,  # Mínimo para máxima flexibilidade
                min_samples_leaf=1,   # Mínimo para máxima flexibilidade
                random_state=42,
                n_jobs=-1,         # Paralelizar máximo para velocidade
                verbose=0,
                max_features='sqrt',
                bootstrap=True,
                oob_score=False,   # Desabilitado para velocidade
                warm_start=False   # Desabilitado para velocidade
            )),
            ('gb', GradientBoostingRegressor(
                n_estimators=300,  # Aumentado para melhor acurácia
                max_depth=12,      # Profundidade aumentada
                learning_rate=0.04,  # Learning rate otimizado (balanceado)
                min_samples_split=2,  # Mínimo para máxima flexibilidade
                min_samples_leaf=1,   # Mínimo para máxima flexibilidade
                random_state=42,
                verbose=0,
                subsample=0.9,        # Subsampling otimizado
                max_features='sqrt',  # Para melhor performance
                validation_fraction=0.1,  # Validação interna
                n_iter_no_change=20   # Early stopping mais tolerante
            ))
        ]
        
        # Adicionar XGBoost se disponível
        if XGBOOST_AVAILABLE:
            models.append(('xgb', xgb.XGBRegressor(
                n_estimators=300,  # Aumentado para melhor acurácia
                max_depth=12,      # Profundidade aumentada
                learning_rate=0.04,  # Learning rate otimizado
                random_state=42,
                n_jobs=-1,         # Paralelizar máximo
                verbosity=0,
                subsample=0.9,        # Subsampling otimizado
                colsample_bytree=0.9, # Feature sampling otimizado
                reg_alpha=0.05,       # Regularização L1 (reduzida)
                reg_lambda=0.5,       # Regularização L2 (reduzida)
                gamma=0,
                min_child_weight=1,    # Mínimo para máxima flexibilidade
                early_stopping_rounds=20  # Early stopping
            )))
        
        # Adicionar modelos lineares (otimizados para melhor acurácia)
        models.extend([
            ('ridge', Ridge(alpha=0.3)),  # Reduzido para melhor acurácia
            ('lasso', Lasso(alpha=0.01, max_iter=2000))  # Reduzido + mais iterações
        ])
        
        return models
    
    def create_ensemble_model(self, X_train, y_train):
        """
        Cria e treina um modelo ensemble otimizado usando StackingRegressor
        para máxima acurácia.
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            
        Returns:
            Modelo treinado
        """
        print("🏗️ Criando modelo ensemble de regressão (Stacking)...")
        
        # Criar modelos base
        base_models = self.create_base_models()
        
        # Criar meta-learner otimizado (modelo que combina os outros)
        meta_learner = Ridge(alpha=0.3)  # Alpha reduzido para melhor acurácia
        
        try:
            ensemble = StackingRegressor(
                estimators=base_models,
                final_estimator=meta_learner,
                cv=3,  # Reduzido de 5 para 3 (mais rápido, ainda eficaz)
                n_jobs=-1,  # Paralelizar máximo
                verbose=0,
                passthrough=False  # Não passar features originais (mais rápido)
            )
            print("✅ Modelo ensemble Stacking criado (máxima acurácia)!")
        except Exception as e:
            print(f"⚠️ Erro ao criar StackingRegressor, usando VotingRegressor: {e}")
            # Fallback para VotingRegressor
            n_models = len(base_models)
            if n_models == 4:  # RF, GB, Ridge, Lasso
                weights = [5, 5, 1, 1]  # Pesos otimizados (RF e GB mais importantes)
            elif n_models == 5:  # RF, GB, XGB, Ridge, Lasso
                weights = [5, 5, 5, 1, 1]  # Pesos otimizados
            else:
                weights = None
            
            ensemble = VotingRegressor(
                estimators=base_models,
                weights=weights,
                n_jobs=-1
            )
            print("✅ Modelo ensemble Voting criado!")
        
        return ensemble
    
    def optimize_model(self, X_train, y_train, model_type='ensemble'):
        """
        Otimiza hiperparâmetros do modelo usando GridSearch.
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            model_type: Tipo de modelo ('ensemble', 'rf', 'gb')
            
        Returns:
            Melhor modelo encontrado
        """
        print(f"🔍 Otimizando modelo {model_type}...")
        
        if model_type == 'rf':
            model = RandomForestRegressor(random_state=42, n_jobs=-1, verbose=0)
            param_grid = {
                'n_estimators': [250, 300, 350],  # Valores mais altos
                'max_depth': [20, 25, 30],        # Valores mais altos
                'min_samples_split': [2, 3, 4],
                'min_samples_leaf': [1, 2],
                'max_features': ['sqrt', 'log2']  # Adicionado
            }
        elif model_type == 'gb':
            model = GradientBoostingRegressor(random_state=42, verbose=0)
            param_grid = {
                'n_estimators': [250, 300, 350],  # Valores mais altos
                'max_depth': [8, 10, 12],         # Valores mais altos
                'learning_rate': [0.02, 0.03, 0.05],  # Valores mais baixos
                'min_samples_split': [2, 3, 4],
                'subsample': [0.8, 0.9, 1.0]      # Adicionado
            }
        else:
            # Para ensemble, usar modelo padrão (GridSearch é muito lento)
            return self.create_ensemble_model(X_train, y_train)
        
        # GridSearch com validação cruzada
        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=3,
            scoring='neg_mean_absolute_error',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train.ravel())
        
        print(f"✅ Melhor score: {-grid_search.best_score_:.4f}")
        print(f"✅ Melhores parâmetros: {grid_search.best_params_}")
        
        return grid_search.best_estimator_
    
    def train(self, X_train, y_train, X_val, y_val, optimize=False, model_type='ensemble'):
        """
        Treina o modelo de regressão.
        
        Args:
            X_train: Features de treino
            y_train: Target de treino
            X_val: Features de validação
            y_val: Target de validação
            optimize: Se True, otimiza hiperparâmetros
            model_type: Tipo de modelo ('ensemble', 'rf', 'gb')
        """
        print(f"\n🚀 Iniciando treinamento do modelo {model_type}...")
        print(f"⚙️ Dados de treino: {X_train.shape}")
        print(f"⚙️ Dados de validação: {X_val.shape}")
        
        # Ajustar formato do target se necessário
        if len(y_train.shape) > 1:
            y_train = y_train.ravel()
        if len(y_val.shape) > 1:
            y_val = y_val.ravel()
        
        # Criar ou otimizar modelo
        if optimize:
            self.model = self.optimize_model(X_train, y_train, model_type)
        else:
            if model_type == 'ensemble':
                self.model = self.create_ensemble_model(X_train, y_train)
            elif model_type == 'rf':
                self.model = RandomForestRegressor(
                    n_estimators=300,  # Aumentado para melhor acurácia
                    max_depth=30,      # Profundidade máxima
                    min_samples_split=2,  # Mínimo para máxima flexibilidade
                    min_samples_leaf=1,   # Mínimo para máxima flexibilidade
                    random_state=42,
                    n_jobs=-1,         # Paralelizar máximo
                    verbose=0,
                    max_features='sqrt',
                    bootstrap=True,
                    oob_score=False    # Desabilitado para velocidade
                )
            elif model_type == 'gb':
                self.model = GradientBoostingRegressor(
                    n_estimators=300,  # Aumentado para melhor acurácia
                    max_depth=12,      # Profundidade aumentada
                    learning_rate=0.04,  # Learning rate otimizado
                    min_samples_split=2,  # Mínimo para máxima flexibilidade
                    min_samples_leaf=1,   # Mínimo para máxima flexibilidade
                    random_state=42,
                    verbose=0,
                    subsample=0.9,        # Subsampling otimizado
                    max_features='sqrt',   # Feature sampling
                    validation_fraction=0.1,
                    n_iter_no_change=20
                )
        
        # Treinar modelo
        print("🎯 Treinando modelo...")
        self.model.fit(X_train, y_train)
        
        # Avaliar no conjunto de validação
        y_pred_val = self.model.predict(X_val)
        mae = mean_absolute_error(y_val, y_pred_val)
        rmse = np.sqrt(mean_squared_error(y_val, y_pred_val))
        r2 = r2_score(y_val, y_pred_val)
        
        print("\n✅ Treinamento concluído!")
        print(f"📊 Métricas de validação:")
        print(f"  MAE: {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  R²: {r2:.4f}")
        
        self.model_name = model_type
        self.best_score = mae
        
        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
    
    def evaluate(self, X_test, y_test):
        """
        Avalia o modelo no conjunto de teste.
        
        Args:
            X_test: Features de teste
            y_test: Target de teste
            
        Returns:
            Dicionário com métricas
        """
        print("\n📊 Avaliando modelo no conjunto de teste...")
        
        if len(y_test.shape) > 1:
            y_test = y_test.ravel()
        
        y_pred = self.model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100
        
        print(f"✅ MAE: {mae:.4f}")
        print(f"✅ RMSE: {rmse:.4f}")
        print(f"✅ R²: {r2:.4f}")
        print(f"✅ MAPE: {mape:.2f}%")
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2,
            'mape': mape
        }
    
    def predict(self, X):
        """
        Faz previsões.
        
        Args:
            X: Features (n_samples, n_features)
            
        Returns:
            Previsões (n_samples,)
        """
        return self.model.predict(X)
    
    def save_model(self, filepath='src/model/saved_models/regression_model.pkl'):
        """
        Salva o modelo treinado.
        
        Args:
            filepath: Caminho para salvar o modelo
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"💾 Modelo salvo em: {filepath}")
    
    def load_model(self, filepath='src/model/saved_models/regression_model.pkl'):
        """
        Carrega um modelo salvo.
        
        Args:
            filepath: Caminho do modelo salvo
        """
        self.model = joblib.load(filepath)
        print(f"📂 Modelo carregado de: {filepath}")
    
    def get_model_info(self):
        """
        Retorna informações sobre o modelo.
        
        Returns:
            Dicionário com informações do modelo
        """
        if self.model is None:
            return {
                'status': 'not_trained',
                'message': 'Modelo não foi treinado ainda.'
            }
        
        info = {
            'model_type': self.model_name or 'ensemble',
            'status': 'trained'
        }
        
        # Informações específicas por tipo de modelo
        if hasattr(self.model, 'n_estimators'):
            info['n_estimators'] = self.model.n_estimators
        if hasattr(self.model, 'estimators_'):
            info['n_base_models'] = len(self.model.estimators_)
        if hasattr(self.model, 'feature_importances_'):
            info['n_features'] = len(self.model.feature_importances_)
        
        return info


def create_default_model():
    """
    Cria um modelo de regressão com configurações padrão otimizadas.
    
    Returns:
        Instância do modelo
    """
    model = EnergyRegressionModel()
    return model


# Importar os para criar diretório
import os

if __name__ == "__main__":
    # Teste da arquitetura
    print("🧪 Testando arquitetura do modelo de regressão...")
    
    model = create_default_model()
    
    # Dados dummy para teste
    X_dummy = np.random.rand(100, 30)
    y_dummy = np.random.rand(100)
    
    print("\n🔍 Testando predição...")
    # Criar modelo simples para teste
    test_model = RandomForestRegressor(n_estimators=10, random_state=42, n_jobs=-1)
    test_model.fit(X_dummy, y_dummy)
    predictions = test_model.predict(X_dummy[:5])
    print(f"✅ Shape das predições: {predictions.shape}")
    
    print("\n✅ Teste concluído!")
