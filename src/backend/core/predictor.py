"""
SERVIÇO DE PREVISÃO
Encapsula a lógica de carregamento do modelo e predição.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Adicionar path do projeto
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.backend.core.config import settings

import gc
import logging
from typing import Optional, Dict, Any

# Configurar logger
logger = logging.getLogger(__name__)

class EnergyPredictor:
    """
    Classe responsável por carregar o modelo e fazer previsões.
    Implementa carregamento preguiçoso para otimização de memória.
    """
    
    def __init__(self, model_path: str, scaler_dir: str):
        """
        Inicializa o preditor com carregamento preguiçoso.
        
        Args:
            model_path: Caminho para o modelo treinado
            scaler_dir: Diretório com os scalers
        """
        self._model = None
        self._preprocessor = None
        self._model_path = model_path
        self._scaler_dir = scaler_dir
        self._is_loaded = False
        
        # Configuração para reduzir uso de memória do joblib
        self._joblib_mmap_mode = 'r'  # Modo de leitura apenas para economizar memória
    
    @property
    def model(self):
        """Carrega o modelo apenas quando necessário."""
        if self._model is None:
            self._load_model()
        return self._model
    
    @property
    def preprocessor(self):
        """Carrega o preprocessor apenas quando necessário."""
        if self._preprocessor is None:
            self._load_preprocessor()
        return self._preprocessor
    
    def _load_model(self):
        """Carrega o modelo de forma preguiçosa."""
        import joblib
        
        if self._model is not None:
            return
            
        try:
            if os.path.exists(self._model_path):
                logger.info(f"Carregando modelo de: {self._model_path}")
                
                # Configuração para reduzir uso de memória
                self._model = joblib.load(
                    self._model_path, 
                    mmap_mode=self._joblib_mmap_mode
                )
                
                self._is_loaded = True
                logger.info("Modelo carregado com sucesso")
                
                # Forçar coleta de lixo após carregar o modelo
                gc.collect()
                
                # Verificar uso de memória
                if hasattr(self._model, 'n_estimators'):
                    logger.info(f"Modelo com {self._model.n_estimators} estimadores")
                
            else:
                logger.error(f"Modelo não encontrado em: {self._model_path}")
                self._is_loaded = False
                
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            self._is_loaded = False
            raise
    
    def _load_preprocessor(self):
        """Carrega o preprocessador de forma preguiçosa."""
        from src.model.preprocessing import EnergyDataPreprocessor
        
        if self._preprocessor is not None:
            return
            
        try:
            logger.info(f"Carregando preprocessador de: {self._scaler_dir}")
            self._preprocessor = EnergyDataPreprocessor()
            self._preprocessor.load_scalers(self._scaler_dir)
            logger.info("Preprocessador carregado com sucesso")
            
            # Forçar coleta de lixo
            gc.collect()
            
        except Exception as e:
            logger.error(f"Erro ao carregar preprocessador: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Verifica se o preditor está pronto para uso."""
        if not self._is_loaded:
            try:
                self._load_model()
                self._load_preprocessor()
            except Exception as e:
                logger.error(f"Erro ao verificar prontidão do modelo: {e}")
                return False
                
        return self._is_loaded and self._model is not None and self._preprocessor is not None
    
    def _prepare_single_prediction_data(self, data: Dict[str, Any]) -> Any:
        """
        Prepara DataFrame completo para previsão única, preenchendo colunas ausentes.
        """
        import pandas as pd
        
        # Valores padrão baseados em médias típicas do dataset
        defaults = {
            'consumption_kwh': data.get('consumption_lag_1h', 1.0),  # Usar lag_1h como base
            'Voltage': 240.0,  # Voltagem típica residencial
            'Global_intensity': 5.0,  # Intensidade típica
            'Sub_metering_1': 0.0,  # Cozinha
            'Sub_metering_2': 0.0,  # Lavanderia
            'Sub_metering_3': 0.0,  # Ar-condicionado/Aquecedor
        }
        
        # Criar DataFrame base
        df_data = {
            'timestamp': pd.Timestamp.now(),
            'temperature_celsius': data.get('temperature_celsius', 25.0),
            'hour': data.get('hour', 12),
            'day_of_week': data.get('day_of_week', 2),
            'month': data.get('month', 6),
            'is_weekend': data.get('is_weekend', 0),
            'is_holiday': data.get('is_holiday', 0),
            'consumption_kwh': defaults['consumption_kwh'],
            'Voltage': defaults['Voltage'],
            'Global_intensity': defaults['Global_intensity'],
            'Sub_metering_1': defaults['Sub_metering_1'],
            'Sub_metering_2': defaults['Sub_metering_2'],
            'Sub_metering_3': defaults['Sub_metering_3'],
            # Usar valores fornecidos para lags e rolling stats
            'consumption_lag_1h': data.get('consumption_lag_1h', defaults['consumption_kwh']),
            'consumption_lag_24h': data.get('consumption_lag_24h', defaults['consumption_kwh']),
            'consumption_lag_168h': data.get('consumption_lag_168h', defaults['consumption_kwh']),
            'consumption_rolling_mean_24h': data.get('consumption_rolling_mean_24h', defaults['consumption_kwh']),
            'consumption_rolling_std_24h': data.get('consumption_rolling_std_24h', 0.1),
        }
        
        df = pd.DataFrame([df_data])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def predict_single(self, data: Dict[str, Any]) -> float:
        """
        Faz uma previsão única.
        
        Args:
            data: Dicionário com os dados de entrada
            
        Returns:
            Previsão de consumo em kWh
        """
        import numpy as np
        
        if not self.is_ready():
            raise RuntimeError("Modelo não está pronto. Treine o modelo primeiro.")
        
        try:
            # Preparar DataFrame completo
            df = self._prepare_single_prediction_data(data)
            
            # Preprocessar - mas sem dropar NaNs (para previsão única)
            df_processed = self._engineer_features_for_prediction(df)
            
            # Preparar features
            X, _ = self.preprocessor.prepare_features(df_processed)
            
            # Normalizar se necessário
            if self.preprocessor.scaler_features is not None:
                X_scaled = self.preprocessor.scaler_features.transform(X)
            else:
                X_scaled = X
            
            # Predição
            y_pred_scaled = self.model.predict(X_scaled)
            
            # Desnormalizar
            if self.preprocessor.scaler_target is not None:
                y_pred = self.preprocessor.inverse_transform_target(y_pred_scaled)
                if len(y_pred.shape) > 1:
                    y_pred = y_pred.ravel()
                pred_value = float(y_pred[0])
            else:
                pred_value = float(y_pred_scaled[0])
            
            # Validar valor
            if not np.isfinite(pred_value) or pred_value < 0:
                pred_value = 1.0  # Valor padrão seguro
            
            return max(0.0, pred_value)
        except Exception as e:
            raise RuntimeError(f"Erro ao fazer previsão: {str(e)}")
    
    def _engineer_features_for_prediction(self, df: Any) -> Any:
        """
        Versão do engineer_features que funciona para previsão única (sem dados históricos).
        """
        import numpy as np
        
        # Garantir que todas as colunas necessárias existam
        if 'Sub_metering_1' not in df.columns:
            df['Sub_metering_1'] = 0.0
        if 'Sub_metering_2' not in df.columns:
            df['Sub_metering_2'] = 0.0
        if 'Sub_metering_3' not in df.columns:
            df['Sub_metering_3'] = 0.0
        if 'Voltage' not in df.columns:
            df['Voltage'] = 240.0
        if 'Global_intensity' not in df.columns:
            df['Global_intensity'] = 5.0
        if 'consumption_kwh' not in df.columns:
            # Usar consumption_lag_1h se disponível, senão usar valor padrão
            if 'consumption_lag_1h' in df.columns:
                df['consumption_kwh'] = df['consumption_lag_1h']
            else:
                df['consumption_kwh'] = 1.0
        
        # Features cíclicas
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['dayofweek_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dayofweek_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Features globais
        df['sub_metering_total'] = (
            df['Sub_metering_1'] + df['Sub_metering_2'] + df['Sub_metering_3']
        )
        
        # Para previsão única, usar os valores fornecidos diretamente
        # (não calcular lags/diffs que requerem histórico)
        if 'consumption_lag_1h' not in df.columns:
            df['consumption_lag_1h'] = df['consumption_kwh']
        if 'consumption_lag_3h' not in df.columns:
            df['consumption_lag_3h'] = df['consumption_lag_1h']
        if 'consumption_lag_24h' not in df.columns:
            df['consumption_lag_24h'] = df['consumption_kwh']
        if 'consumption_lag_168h' not in df.columns:
            df['consumption_lag_168h'] = df['consumption_kwh']
        if 'temperature_lag_24h' not in df.columns:
            df['temperature_lag_24h'] = df['temperature_celsius']
        if 'voltage_lag_1h' not in df.columns:
            df['voltage_lag_1h'] = df['Voltage']
        if 'global_intensity_lag_1h' not in df.columns:
            df['global_intensity_lag_1h'] = df['Global_intensity']
        
        # Diferenças (usar 0 para previsão única)
        df['consumption_diff_1h'] = 0.0
        df['consumption_diff_24h'] = 0.0
        df['consumption_pct_change_24h'] = 0.0
        
        # Rolling stats (usar valores fornecidos ou defaults)
        if 'consumption_rolling_mean_24h' not in df.columns:
            df['consumption_rolling_mean_24h'] = df['consumption_kwh']
        if 'consumption_rolling_std_24h' not in df.columns:
            df['consumption_rolling_std_24h'] = 0.1
        if 'consumption_rolling_mean_168h' not in df.columns:
            df['consumption_rolling_mean_168h'] = df['consumption_kwh']
        if 'consumption_rolling_std_168h' not in df.columns:
            df['consumption_rolling_std_168h'] = 0.1
        
        # Limpar inf/nan
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(0)  # Preencher NaNs com 0 ao invés de dropar
        
        return df
    
    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[float]:
        """
        Faz previsões em lote.
        
        Args:
            data_list: Lista de dicionários com dados
            
        Returns:
            Lista de previsões
        """
        if not self.is_ready():
            raise RuntimeError("Modelo não está pronto. Treine o modelo primeiro.")
        
        predictions = []
        for data in data_list:
            try:
                pred = self.predict_single(data)
                predictions.append(pred)
            except Exception as e:
                print(f"Erro na previsão: {e}")
                predictions.append(None)
        
        return predictions
    
    def predict_next_hours(self, historical_data: Any, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Prevê as próximas N horas baseado em dados históricos.
        Atualiza features temporais (hora, dia, mês) e lags para cada hora futura.
        
        Args:
            historical_data: DataFrame com dados históricos
            hours: Número de horas para prever
            
        Returns:
            Lista de previsões com timestamp
        """
        import pandas as pd
        import numpy as np
        
        if not self.is_ready():
            raise RuntimeError("Modelo não está pronto. Treine o modelo primeiro.")
        
        # Preprocessar dados históricos para obter últimas observações
        df_processed = self.preprocessor.engineer_features(historical_data.copy())
        
        # Obter último registro como base
        last_row = df_processed.iloc[-1].copy()
        last_timestamp = historical_data['timestamp'].max()
        
        # Preparar lista de previsões anteriores (para atualizar lags)
        prediction_history = []
        
        # Adicionar últimas 168 horas de consumo real para inicializar lags
        if 'consumption_kwh' in df_processed.columns:
            recent_consumption = df_processed['consumption_kwh'].tail(168).tolist()
            prediction_history = recent_consumption
        
        predictions = []
        
        for i in range(hours):
            # Calcular próximo timestamp
            next_timestamp = last_timestamp + pd.Timedelta(hours=i+1)
            
            # Extrair features temporais do novo timestamp
            next_hour = next_timestamp.hour
            next_day_of_week = next_timestamp.dayofweek  # 0=Segunda, 6=Domingo
            next_month = next_timestamp.month
            next_is_weekend = 1 if next_day_of_week >= 5 else 0
            next_is_holiday = 0  # Assumir não é feriado (pode ser melhorado)
            
            # Criar novo registro com features atualizadas
            new_row = last_row.copy()
            
            # Atualizar features temporais
            new_row['hour'] = next_hour
            new_row['day_of_week'] = next_day_of_week
            new_row['month'] = next_month
            new_row['is_weekend'] = next_is_weekend
            new_row['is_holiday'] = next_is_holiday
            new_row['timestamp'] = next_timestamp
            
            # Atualizar features cíclicas baseadas no novo timestamp
            new_row['hour_sin'] = np.sin(2 * np.pi * next_hour / 24)
            new_row['hour_cos'] = np.cos(2 * np.pi * next_hour / 24)
            new_row['month_sin'] = np.sin(2 * np.pi * next_month / 12)
            new_row['month_cos'] = np.cos(2 * np.pi * next_month / 12)
            new_row['dayofweek_sin'] = np.sin(2 * np.pi * next_day_of_week / 7)
            new_row['dayofweek_cos'] = np.cos(2 * np.pi * next_day_of_week / 7)
            
            # Atualizar lags usando histórico de previsões
            if len(prediction_history) >= 1:
                new_row['consumption_lag_1h'] = prediction_history[-1]
            else:
                new_row['consumption_lag_1h'] = last_row.get('consumption_lag_1h', 1.0) if 'consumption_lag_1h' in last_row else (last_row.get('consumption_kwh', 1.0) if 'consumption_kwh' in last_row else 1.0)
            
            if len(prediction_history) >= 24:
                new_row['consumption_lag_24h'] = prediction_history[-24]
            else:
                new_row['consumption_lag_24h'] = last_row.get('consumption_lag_24h', 1.0) if 'consumption_lag_24h' in last_row else (last_row.get('consumption_kwh', 1.0) if 'consumption_kwh' in last_row else 1.0)
            
            if len(prediction_history) >= 168:
                new_row['consumption_lag_168h'] = prediction_history[-168]
            else:
                new_row['consumption_lag_168h'] = last_row.get('consumption_lag_168h', 1.0) if 'consumption_lag_168h' in last_row else (last_row.get('consumption_kwh', 1.0) if 'consumption_kwh' in last_row else 1.0)
            
            # Atualizar consumption_lag_3h (usar lag_1h como aproximação)
            new_row['consumption_lag_3h'] = new_row['consumption_lag_1h']
            
            # Atualizar rolling statistics
            if len(prediction_history) >= 24:
                recent_24h = prediction_history[-24:]
                new_row['consumption_rolling_mean_24h'] = float(np.mean(recent_24h))
                new_row['consumption_rolling_std_24h'] = float(np.std(recent_24h)) if len(recent_24h) > 1 else 0.1
            elif len(prediction_history) > 0:
                new_row['consumption_rolling_mean_24h'] = float(np.mean(prediction_history))
                new_row['consumption_rolling_std_24h'] = float(np.std(prediction_history)) if len(prediction_history) > 1 else 0.1
            else:
                new_row['consumption_rolling_mean_24h'] = last_row.get('consumption_rolling_mean_24h', 1.0) if 'consumption_rolling_mean_24h' in last_row else 1.0
                new_row['consumption_rolling_std_24h'] = last_row.get('consumption_rolling_std_24h', 0.1) if 'consumption_rolling_std_24h' in last_row else 0.1
            
            if len(prediction_history) >= 168:
                recent_168h = prediction_history[-168:]
                new_row['consumption_rolling_mean_168h'] = float(np.mean(recent_168h))
                new_row['consumption_rolling_std_168h'] = float(np.std(recent_168h)) if len(recent_168h) > 1 else 0.1
            else:
                new_row['consumption_rolling_mean_168h'] = last_row.get('consumption_rolling_mean_168h', 1.0) if 'consumption_rolling_mean_168h' in last_row else 1.0
                new_row['consumption_rolling_std_168h'] = last_row.get('consumption_rolling_std_168h', 0.1) if 'consumption_rolling_std_168h' in last_row else 0.1
            
            # Atualizar diferenças (usar 0 para previsão futura)
            new_row['consumption_diff_1h'] = 0.0
            new_row['consumption_diff_24h'] = 0.0
            new_row['consumption_pct_change_24h'] = 0.0
            
            # Atualizar temperature_lag_24h (usar temperatura atual como aproximação)
            if 'temperature_celsius' in new_row:
                new_row['temperature_lag_24h'] = new_row['temperature_celsius']
            else:
                new_row['temperature_lag_24h'] = last_row.get('temperature_celsius', 25.0) if 'temperature_celsius' in last_row else 25.0
            
            # Garantir que todas as colunas necessárias existam
            required_cols = {
                'Voltage': 240.0,
                'voltage_lag_1h': 240.0,
                'Global_intensity': 5.0,
                'global_intensity_lag_1h': 5.0,
                'Sub_metering_1': 0.0,
                'Sub_metering_2': 0.0,
                'Sub_metering_3': 0.0,
                'sub_metering_total': 0.0,
                'consumption_kwh': new_row['consumption_lag_1h'] if 'consumption_lag_1h' in new_row else 1.0
            }
            
            for col, default_val in required_cols.items():
                if col not in new_row:
                    new_row[col] = default_val
            
            # Recalcular sub_metering_total
            new_row['sub_metering_total'] = new_row['Sub_metering_1'] + new_row['Sub_metering_2'] + new_row['Sub_metering_3']
            
            # Criar DataFrame com uma única linha para previsão
            df_single = pd.DataFrame([new_row])
            
            # Preparar features para o modelo
            X, _ = self.preprocessor.prepare_features(df_single)
            
            # Normalizar
            if self.preprocessor.scaler_features is not None:
                X_scaled = self.preprocessor.scaler_features.transform(X)
            else:
                X_scaled = X
            
            # Fazer previsão
            y_pred_scaled = self.model.predict(X_scaled)
            
            # Desnormalizar
            if self.preprocessor.scaler_target is not None:
                y_pred = self.preprocessor.inverse_transform_target(y_pred_scaled)
                if len(y_pred.shape) > 1:
                    y_pred = y_pred.ravel()
                pred_value = float(y_pred[0])
            else:
                pred_value = float(y_pred_scaled[0])
            
            # Garantir que o valor seja positivo, razoável e válido
            if not np.isfinite(pred_value) or pred_value < 0:
                # Se o valor for inválido, usar a média do histórico ou valor padrão
                if len(prediction_history) > 0:
                    pred_value = float(np.mean(prediction_history[-24:])) if len(prediction_history) >= 24 else float(np.mean(prediction_history))
                else:
                    pred_value = last_row.get('consumption_kwh', 1.0) if 'consumption_kwh' in last_row else 1.0
                pred_value = max(0.0, pred_value)
            
            pred_value = float(max(0.0, pred_value))
            
            # Adicionar à lista de previsões
            predictions.append({
                'timestamp': next_timestamp.isoformat(),
                'predicted_consumption': pred_value
            })
            
            # Adicionar previsão ao histórico para próximas iterações
            prediction_history.append(pred_value)
            
            # Manter apenas últimas 168 horas no histórico (para eficiência)
            if len(prediction_history) > 168:
                prediction_history = prediction_history[-168:]
        
        return predictions
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o modelo.
        """
        if not self.is_ready():
            return {
                'status': 'not_ready',
                'message': 'Modelo não carregado. Execute o treinamento primeiro.'
            }
        
        info = {
            'status': 'ready',
            'model_path': self._model_path,
            'model_type': 'regression_ml'
        }
        
        # Informações do modelo (para ensemble StackingRegressor/VotingRegressor)
        if hasattr(self.model, 'estimators_'):
            # StackingRegressor ou VotingRegressor
            info['n_base_models'] = len(self.model.estimators_)
            info['model_type'] = 'ensemble'
            
            # Tentar obter n_estimators dos modelos base (se todos tiverem o mesmo)
            try:
                if len(self.model.estimators_) > 0:
                    first_estimator = self.model.estimators_[0][1]  # (nome, modelo)
                    if hasattr(first_estimator, 'n_estimators'):
                        info['n_estimators'] = first_estimator.n_estimators
            except:
                pass
        elif hasattr(self.model, 'n_estimators'):
            # Modelo único (RF, GB, XGB)
            info['n_estimators'] = self.model.n_estimators
            info['model_type'] = getattr(self.model, '__class__', {}).__name__ or 'regression_ml'
        
        # Informações de features
        if hasattr(self.model, 'feature_importances_'):
            info['n_features'] = len(self.model.feature_importances_)
        elif hasattr(self.model, 'n_features_in_'):
            info['n_features'] = self.model.n_features_in_
        
        # Informações do preprocessador (prioridade)
        if self.preprocessor and hasattr(self.preprocessor, 'feature_columns') and self.preprocessor.feature_columns:
            info['n_features'] = len(self.preprocessor.feature_columns)
        
        return info


# Instância global do preditor (singleton)
_predictor_instance = None

def get_predictor_instance() -> EnergyPredictor:
    """
    Retorna a instância singleton do preditor.
    """
    global _predictor_instance
    
    if _predictor_instance is None:
        _predictor_instance = EnergyPredictor(settings.MODEL_PATH, settings.SCALER_DIR)
    
    return _predictor_instance
