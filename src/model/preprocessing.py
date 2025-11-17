"""
PIPELINE DE PREPROCESSAMENTO DE DADOS
Prepara os dados para modelos de regressão ML.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os


class EnergyDataPreprocessor:
    """
    Classe responsável por preprocessar dados de energia para modelos de regressão ML.
    """
    
    def __init__(self, use_scaler='standard'):
        """
        Args:
            use_scaler: Tipo de scaler ('standard', 'minmax', ou None)
        """
        self.use_scaler = use_scaler
        if use_scaler == 'standard':
            self.scaler_features = StandardScaler()
            self.scaler_target = StandardScaler()
        elif use_scaler == 'minmax':
            self.scaler_features = MinMaxScaler()
            self.scaler_target = MinMaxScaler()
        else:
            self.scaler_features = None
            self.scaler_target = None
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
        df['dayofweek_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dayofweek_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
        
        # Features globais adicionais
        df['sub_metering_total'] = (
            df['Sub_metering_1'] + df['Sub_metering_2'] + df['Sub_metering_3']
        )
        
        # Features de lag (consumo e temperatura anteriores)
        df['consumption_lag_1h'] = df['consumption_kwh'].shift(1)
        df['consumption_lag_3h'] = df['consumption_kwh'].shift(3)
        df['consumption_lag_24h'] = df['consumption_kwh'].shift(24)
        df['consumption_lag_168h'] = df['consumption_kwh'].shift(168)  # 1 semana
        df['temperature_lag_24h'] = df['temperature_celsius'].shift(24)
        df['voltage_lag_1h'] = df['Voltage'].shift(1)
        df['global_intensity_lag_1h'] = df['Global_intensity'].shift(1)
        
        # Diferenças e tendências
        df['consumption_diff_1h'] = df['consumption_kwh'].diff(1)
        df['consumption_diff_24h'] = df['consumption_kwh'].diff(24)
        df['consumption_pct_change_24h'] = df['consumption_kwh'].pct_change(24)
        
        # Rolling statistics
        df['consumption_rolling_mean_24h'] = df['consumption_kwh'].rolling(window=24, min_periods=1).mean()
        df['consumption_rolling_std_24h'] = df['consumption_kwh'].rolling(window=24, min_periods=1).std()
        df['consumption_rolling_mean_168h'] = df['consumption_kwh'].rolling(window=168, min_periods=1).mean()
        df['consumption_rolling_std_168h'] = df['consumption_kwh'].rolling(window=168, min_periods=1).std()
        
        # Remover NaNs criados pelos lags
        df = df.replace([np.inf, -np.inf], np.nan)
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
            'temperature_lag_24h',
            'hour_sin', 'hour_cos',
            'month_sin', 'month_cos',
            'dayofweek_sin', 'dayofweek_cos',
            'day_of_week',
            'is_weekend',
            'is_holiday',
            'Voltage',
            'voltage_lag_1h',
            'Global_intensity',
            'global_intensity_lag_1h',
            'Sub_metering_1',
            'Sub_metering_2',
            'Sub_metering_3',
            'sub_metering_total',
            'consumption_lag_1h',
            'consumption_lag_3h',
            'consumption_lag_24h',
            'consumption_lag_168h',
            'consumption_diff_1h',
            'consumption_diff_24h',
            'consumption_pct_change_24h',
            'consumption_rolling_mean_24h',
            'consumption_rolling_std_24h',
            'consumption_rolling_mean_168h',
            'consumption_rolling_std_168h'
        ]
        
        X = df[self.feature_columns].values
        y = df['consumption_kwh'].values.reshape(-1, 1)
        
        return X, y
    
    def prepare_for_regression(self, X, y):
        """
        Prepara dados para regressão (sem sequências temporais).
        
        Args:
            X: Features (n_samples, n_features)
            y: Target (n_samples, 1)
            
        Returns:
            X: Features preparadas (n_samples, n_features)
            y: Target preparado (n_samples,)
        """
        # Ajustar formato do target
        if len(y.shape) > 1:
            y = y.ravel()
        
        return X, y
    
    def fit_transform(self, df):
        """
        Pipeline completo de preprocessamento para regressão.
        """
        # Engenharia de features
        df = self.engineer_features(df)
        
        # Preparar features e target
        X, y = self.prepare_features(df)
        
        # Normalizar dados (se scaler foi configurado)
        if self.scaler_features is not None:
            print("📊 Normalizando dados...")
            X_scaled = self.scaler_features.fit_transform(X)
            y_scaled = self.scaler_target.fit_transform(y.reshape(-1, 1))
            y_scaled = y_scaled.ravel()
        else:
            X_scaled = X
            y_scaled = y.ravel()
        
        # Preparar para regressão (sem sequências)
        X_prep, y_prep = self.prepare_for_regression(X_scaled, y_scaled)
        
        # Split train/test (usando TODOS os dados disponíveis)
        print("✂️ Dividindo em treino e teste...")
        print(f"📊 Total de dados disponíveis: {len(X_prep):,} amostras")
        X_train, X_test, y_train, y_test = train_test_split(
            X_prep, y_prep, test_size=0.2, shuffle=True, random_state=42
        )
        print(f"✅ Usando TODOS os dados disponíveis (sem limitações)")
        
        print(f"✅ Treino: {X_train.shape[0]:,} amostras")
        print(f"✅ Teste: {X_test.shape[0]:,} amostras")
        print(f"✅ Features: {X_train.shape[1]} colunas")
        
        return X_train, X_test, y_train, y_test
    
    def transform(self, df):
        """
        Transforma novos dados usando os scalers já ajustados.
        """
        df = self.engineer_features(df)
        X, y = self.prepare_features(df)
        
        if self.scaler_features is not None:
            X_scaled = self.scaler_features.transform(X)
            y_scaled = self.scaler_target.transform(y.reshape(-1, 1))
            y_scaled = y_scaled.ravel()
        else:
            X_scaled = X
            y_scaled = y.ravel()
        
        X_prep, y_prep = self.prepare_for_regression(X_scaled, y_scaled)
        return X_prep, y_prep
    
    def inverse_transform_target(self, y_scaled):
        """
        Reverte a normalização do target.
        """
        if self.scaler_target is not None:
            if len(y_scaled.shape) == 1:
                y_scaled = y_scaled.reshape(-1, 1)
            return self.scaler_target.inverse_transform(y_scaled)
        else:
            return y_scaled
    
    def save_scalers(self, output_dir='src/model/saved_models'):
        """
        Salva os scalers para uso em produção.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        if self.scaler_features is not None:
            joblib.dump(self.scaler_features, f'{output_dir}/scaler_features.pkl')
            joblib.dump(self.scaler_target, f'{output_dir}/scaler_target.pkl')
        joblib.dump(self.feature_columns, f'{output_dir}/feature_columns.pkl')
        joblib.dump(self.use_scaler, f'{output_dir}/scaler_type.pkl')
        
        print(f"💾 Scalers salvos em: {output_dir}")
    
    def load_scalers(self, input_dir='src/model/saved_models'):
        """
        Carrega scalers salvos.
        """
        feature_columns_path = f'{input_dir}/feature_columns.pkl'
        if os.path.exists(feature_columns_path):
            self.feature_columns = joblib.load(feature_columns_path)
        else:
            self.feature_columns = None
            print(f"⚠️ Arquivo feature_columns.pkl não encontrado em: {input_dir}")
        
        scaler_type_path = f'{input_dir}/scaler_type.pkl'
        if os.path.exists(scaler_type_path):
            self.use_scaler = joblib.load(scaler_type_path)
        else:
            self.use_scaler = 'standard'
        
        scaler_features_path = f'{input_dir}/scaler_features.pkl'
        if os.path.exists(scaler_features_path):
            self.scaler_features = joblib.load(scaler_features_path)
            scaler_target_path = f'{input_dir}/scaler_target.pkl'
            if os.path.exists(scaler_target_path):
                self.scaler_target = joblib.load(scaler_target_path)
            else:
                self.scaler_target = None
        else:
            self.scaler_features = None
            self.scaler_target = None
        
        if self.feature_columns and self.scaler_features:
            print(f"📂 Scalers carregados de: {input_dir}")
        else:
            print(f"⚠️ Alguns scalers não foram encontrados em: {input_dir}")


if __name__ == "__main__":
    # Teste do preprocessador
    preprocessor = EnergyDataPreprocessor(use_scaler='standard')
    
    # Carregar dados
    df = preprocessor.load_data('data/raw/energy_consumption.csv')
    
    # Preprocessar
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    
    # Salvar scalers
    preprocessor.save_scalers()
    
    print("\n✅ Preprocessamento concluído!")
