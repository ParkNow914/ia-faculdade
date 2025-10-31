"""
PIPELINE DE PREPROCESSAMENTO DE DADOS
Prepara os dados de séries temporais para o modelo LSTM.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib
import os


class EnergyDataPreprocessor:
    """
    Classe responsável por preprocessar dados de energia para o modelo LSTM.
    """
    
    def __init__(self, sequence_length=24):
        """
        Args:
            sequence_length: Número de timesteps passados para prever o próximo valor
        """
        self.sequence_length = sequence_length
        self.scaler_features = MinMaxScaler()
        self.scaler_target = MinMaxScaler()
        self.feature_columns = None
        
    def load_data(self, file_path):
        """Carrega o dataset de energia."""
        print(f"📂 Carregando dados de: {file_path}")
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        print(f"✅ {len(df):,} registros carregados")
        return df
    
    def engineer_features(self, df):
        """
        Engenharia de features temporais adicionais.
        """
        print("🔧 Engenharia de features...")
        
        # Features cíclicas (hora e mês)
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        # Features de lag (consumo anterior)
        df['consumption_lag_1h'] = df['consumption_kwh'].shift(1)
        df['consumption_lag_24h'] = df['consumption_kwh'].shift(24)
        df['consumption_lag_168h'] = df['consumption_kwh'].shift(168)  # 1 semana
        
        # Rolling statistics
        df['consumption_rolling_mean_24h'] = df['consumption_kwh'].rolling(window=24, min_periods=1).mean()
        df['consumption_rolling_std_24h'] = df['consumption_kwh'].rolling(window=24, min_periods=1).std()
        
        # Remover NaNs criados pelos lags
        df = df.dropna()
        
        print(f"✅ Features criadas. Total de colunas: {len(df.columns)}")
        return df
    
    def prepare_features(self, df):
        """
        Seleciona e prepara features para o modelo.
        """
        # Features para o modelo
        self.feature_columns = [
            'temperature_celsius',
            'hour_sin', 'hour_cos',
            'month_sin', 'month_cos',
            'day_of_week',
            'is_weekend',
            'is_holiday',
            'consumption_lag_1h',
            'consumption_lag_24h',
            'consumption_lag_168h',
            'consumption_rolling_mean_24h',
            'consumption_rolling_std_24h'
        ]
        
        X = df[self.feature_columns].values
        y = df['consumption_kwh'].values.reshape(-1, 1)
        
        return X, y
    
    def create_sequences(self, X, y):
        """
        Cria sequências temporais para o LSTM.
        
        Args:
            X: Features (n_samples, n_features)
            y: Target (n_samples, 1)
            
        Returns:
            X_seq: (n_sequences, sequence_length, n_features)
            y_seq: (n_sequences, 1)
        """
        print(f"🔄 Criando sequências de {self.sequence_length} timesteps...")
        
        X_seq = []
        y_seq = []
        
        for i in range(self.sequence_length, len(X)):
            X_seq.append(X[i - self.sequence_length:i])
            y_seq.append(y[i])
        
        X_seq = np.array(X_seq)
        y_seq = np.array(y_seq)
        
        print(f"✅ Sequências criadas: {X_seq.shape}")
        return X_seq, y_seq
    
    def fit_transform(self, df):
        """
        Pipeline completo de preprocessamento.
        """
        # Engenharia de features
        df = self.engineer_features(df)
        
        # Preparar features e target
        X, y = self.prepare_features(df)
        
        # Normalizar dados
        print("📊 Normalizando dados...")
        X_scaled = self.scaler_features.fit_transform(X)
        y_scaled = self.scaler_target.fit_transform(y)
        
        # Criar sequências
        X_seq, y_seq = self.create_sequences(X_scaled, y_scaled)
        
        # Split train/test
        print("✂️ Dividindo em treino e teste...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_seq, y_seq, test_size=0.2, shuffle=False
        )
        
        print(f"✅ Treino: {X_train.shape[0]:,} amostras")
        print(f"✅ Teste: {X_test.shape[0]:,} amostras")
        
        return X_train, X_test, y_train, y_test
    
    def transform(self, df):
        """
        Transforma novos dados usando os scalers já ajustados.
        """
        df = self.engineer_features(df)
        X, y = self.prepare_features(df)
        X_scaled = self.scaler_features.transform(X)
        y_scaled = self.scaler_target.transform(y)
        X_seq, y_seq = self.create_sequences(X_scaled, y_scaled)
        return X_seq, y_seq
    
    def inverse_transform_target(self, y_scaled):
        """
        Reverte a normalização do target.
        """
        return self.scaler_target.inverse_transform(y_scaled)
    
    def save_scalers(self, output_dir='src/model/saved_models'):
        """
        Salva os scalers para uso em produção.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        joblib.dump(self.scaler_features, f'{output_dir}/scaler_features.pkl')
        joblib.dump(self.scaler_target, f'{output_dir}/scaler_target.pkl')
        joblib.dump(self.feature_columns, f'{output_dir}/feature_columns.pkl')
        joblib.dump(self.sequence_length, f'{output_dir}/sequence_length.pkl')
        
        print(f"💾 Scalers salvos em: {output_dir}")
    
    def load_scalers(self, input_dir='src/model/saved_models'):
        """
        Carrega scalers salvos.
        """
        self.scaler_features = joblib.load(f'{input_dir}/scaler_features.pkl')
        self.scaler_target = joblib.load(f'{input_dir}/scaler_target.pkl')
        self.feature_columns = joblib.load(f'{input_dir}/feature_columns.pkl')
        self.sequence_length = joblib.load(f'{input_dir}/sequence_length.pkl')
        
        print(f"📂 Scalers carregados de: {input_dir}")


if __name__ == "__main__":
    # Teste do preprocessador
    preprocessor = EnergyDataPreprocessor(sequence_length=24)
    
    # Carregar dados
    df = preprocessor.load_data('data/raw/energy_consumption.csv')
    
    # Preprocessar
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    
    # Salvar scalers
    preprocessor.save_scalers()
    
    print("\n✅ Preprocessamento concluído!")
