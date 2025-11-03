"""
SERVIÇO DE PREVISÃO
Encapsula a lógica de carregamento do modelo e predição.
"""

import os
import sys
from pathlib import Path
import numpy as np
import joblib
from tensorflow import keras
from typing import List, Dict, Any
import pandas as pd

# Adicionar path do projeto
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.model.preprocessing import EnergyDataPreprocessor


class EnergyPredictor:
    """
    Classe responsável por carregar o modelo e fazer previsões.
    """
    
    def __init__(self, model_path: str, scaler_dir: str):
        """
        Inicializa o preditor.
        
        Args:
            model_path: Caminho para o modelo treinado
            scaler_dir: Diretório com os scalers
        """
        self.model = None
        self.preprocessor = None
        self.model_path = model_path
        self.scaler_dir = scaler_dir
        
        self._load_model()
        self._load_preprocessor()
    
    def _load_model(self):
        """Carrega o modelo LSTM."""
        try:
            if os.path.exists(self.model_path):
                # Tentar carregar com compile=False para Keras 3
                self.model = keras.models.load_model(self.model_path, compile=False)
                # Recompilar manualmente
                self.model.compile(
                    optimizer='adam',
                    loss='mse',
                    metrics=['mae', 'mape']
                )
                print(f"✅ Modelo carregado de: {self.model_path}")
            else:
                print(f"⚠️ Modelo não encontrado em: {self.model_path}")
                print("ℹ️ Execute 'python src/model/train.py' primeiro!")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
    
    def _load_preprocessor(self):
        """Carrega o preprocessador."""
        try:
            self.preprocessor = EnergyDataPreprocessor()
            self.preprocessor.load_scalers(self.scaler_dir)
            print(f"✅ Preprocessador carregado de: {self.scaler_dir}")
        except Exception as e:
            print(f"❌ Erro ao carregar preprocessador: {e}")
    
    def is_ready(self) -> bool:
        """Verifica se o preditor está pronto."""
        return self.model is not None and self.preprocessor is not None
    
    def predict_single(self, data: Dict[str, Any]) -> float:
        """
        Faz uma previsão única.
        
        Args:
            data: Dicionário com os dados de entrada
            
        Returns:
            Previsão de consumo em kWh
        """
        if not self.is_ready():
            raise RuntimeError("Modelo não está pronto. Treine o modelo primeiro.")
        
        # Criar DataFrame com os dados
        df = pd.DataFrame([data])
        
        # Preprocessar
        df_processed = self.preprocessor.engineer_features(df)
        X, _ = self.preprocessor.prepare_features(df_processed)
        X_scaled = self.preprocessor.scaler_features.transform(X)
        
        # Criar sequência (pegar últimas 24 horas)
        if len(X_scaled) < self.preprocessor.sequence_length:
            raise ValueError(f"Necessário pelo menos {self.preprocessor.sequence_length} timesteps")
        
        X_seq = X_scaled[-self.preprocessor.sequence_length:]
        X_seq = np.array([X_seq])
        
        # Predição
        y_pred_scaled = self.model.predict(X_seq, verbose=0)
        y_pred = self.preprocessor.inverse_transform_target(y_pred_scaled)
        
        return float(y_pred[0][0])
    
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
    
    def predict_next_hours(self, historical_data: pd.DataFrame, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Prevê as próximas N horas baseado em dados históricos.
        
        Args:
            historical_data: DataFrame com dados históricos
            hours: Número de horas para prever
            
        Returns:
            Lista de previsões com timestamp
        """
        if not self.is_ready():
            raise RuntimeError("Modelo não está pronto. Treine o modelo primeiro.")
        
        # Preprocessar dados históricos
        df_processed = self.preprocessor.engineer_features(historical_data.copy())
        X, y = self.preprocessor.prepare_features(df_processed)
        X_scaled = self.preprocessor.scaler_features.transform(X)
        
        predictions = []
        last_timestamp = historical_data['timestamp'].max()
        
        # Usar últimas 24 horas como base
        current_sequence = X_scaled[-self.preprocessor.sequence_length:]
        
        for i in range(hours):
            # Fazer previsão
            X_seq = np.array([current_sequence])
            y_pred_scaled = self.model.predict(X_seq, verbose=0)
            y_pred = self.preprocessor.inverse_transform_target(y_pred_scaled)
            
            # Próximo timestamp
            next_timestamp = last_timestamp + pd.Timedelta(hours=i+1)
            
            predictions.append({
                'timestamp': next_timestamp.isoformat(),
                'predicted_consumption': float(y_pred[0][0])
            })
            
            # Atualizar sequência (sliding window)
            # Nota: Em produção real, você adicionaria features reais do próximo timestep
            # Aqui simplificamos usando a última observação
            current_sequence = np.roll(current_sequence, -1, axis=0)
            current_sequence[-1] = X_scaled[-1]  # Placeholder
        
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
        
        return {
            'status': 'ready',
            'model_path': self.model_path,
            'input_shape': str(self.model.input_shape),
            'output_shape': str(self.model.output_shape),
            'total_params': self.model.count_params(),
            'sequence_length': self.preprocessor.sequence_length,
            'n_features': len(self.preprocessor.feature_columns)
        }


# Instância global do preditor (singleton)
_predictor_instance = None

def get_predictor(model_path: str, scaler_dir: str) -> EnergyPredictor:
    """
    Retorna a instância singleton do preditor.
    """
    global _predictor_instance
    
    if _predictor_instance is None:
        _predictor_instance = EnergyPredictor(model_path, scaler_dir)
    
    return _predictor_instance
