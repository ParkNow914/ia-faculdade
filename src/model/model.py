"""
ARQUITETURA DO MODELO LSTM PARA PREVISÃO DE ENERGIA
Rede Neural Recorrente com Long Short-Term Memory.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np


class EnergyLSTMModel:
    """
    Modelo LSTM para previsão de consumo de energia elétrica.
    """
    
    def __init__(self, sequence_length=24, n_features=13):
        """
        Args:
            sequence_length: Número de timesteps de entrada
            n_features: Número de features por timestep
        """
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        self.history = None
        
    def build_model(self, lstm_units=[128, 64, 32], dropout_rate=0.2):
        """
        Constrói a arquitetura do modelo LSTM.
        
        Args:
            lstm_units: Lista com número de unidades em cada camada LSTM
            dropout_rate: Taxa de dropout para regularização
        """
        print("🏗️ Construindo arquitetura do modelo LSTM...")
        
        model = models.Sequential(name='EnergyLSTM')
        
        # === INPUT LAYER ===
        model.add(layers.Input(shape=(self.sequence_length, self.n_features)))
        
        # === LSTM LAYERS ===
        # Primeira camada LSTM (retorna sequências)
        model.add(layers.LSTM(
            units=lstm_units[0],
            return_sequences=True,
            name='lstm_1'
        ))
        model.add(layers.Dropout(dropout_rate, name='dropout_1'))
        model.add(layers.BatchNormalization(name='batch_norm_1'))
        
        # Segunda camada LSTM (retorna sequências)
        if len(lstm_units) > 1:
            model.add(layers.LSTM(
                units=lstm_units[1],
                return_sequences=True,
                name='lstm_2'
            ))
            model.add(layers.Dropout(dropout_rate, name='dropout_2'))
            model.add(layers.BatchNormalization(name='batch_norm_2'))
        
        # Terceira camada LSTM (não retorna sequências)
        if len(lstm_units) > 2:
            model.add(layers.LSTM(
                units=lstm_units[2],
                return_sequences=False,
                name='lstm_3'
            ))
            model.add(layers.Dropout(dropout_rate, name='dropout_3'))
            model.add(layers.BatchNormalization(name='batch_norm_3'))
        
        # === DENSE LAYERS ===
        model.add(layers.Dense(64, activation='relu', name='dense_1'))
        model.add(layers.Dropout(dropout_rate / 2, name='dropout_dense'))
        
        model.add(layers.Dense(32, activation='relu', name='dense_2'))
        
        # === OUTPUT LAYER ===
        model.add(layers.Dense(1, activation='linear', name='output'))
        
        # === COMPILAR MODELO ===
        optimizer = keras.optimizers.Adam(learning_rate=0.001)
        
        model.compile(
            optimizer=optimizer,
            loss='mse',
            metrics=['mae', 'mape']
        )
        
        self.model = model
        
        print("✅ Modelo construído com sucesso!")
        print(f"\n📊 Resumo da arquitetura:")
        model.summary()
        
        return model
    
    def train(self, X_train, y_train, X_val, y_val, 
              epochs=100, batch_size=32, verbose=1):
        """
        Treina o modelo LSTM.
        
        Args:
            X_train: Dados de treino
            y_train: Labels de treino
            X_val: Dados de validação
            y_val: Labels de validação
            epochs: Número de épocas
            batch_size: Tamanho do batch
        """
        print(f"\n🚀 Iniciando treinamento...")
        print(f"⚙️ Épocas: {epochs} | Batch size: {batch_size}")
        
        # === CALLBACKS ===
        callbacks = [
            # Early Stopping
            EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            
            # Model Checkpoint
            ModelCheckpoint(
                filepath='src/model/saved_models/best_model.h5',
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            ),
            
            # Reduce Learning Rate
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=7,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # === TREINAMENTO ===
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose
        )
        
        print("\n✅ Treinamento concluído!")
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """
        Avalia o modelo no conjunto de teste.
        """
        print("\n📊 Avaliando modelo no conjunto de teste...")
        
        results = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"✅ Loss (MSE): {results[0]:.4f}")
        print(f"✅ MAE: {results[1]:.4f}")
        print(f"✅ MAPE: {results[2]:.2f}%")
        
        return results
    
    def predict(self, X):
        """
        Faz previsões.
        """
        return self.model.predict(X, verbose=0)
    
    def save_model(self, filepath='src/model/saved_models/lstm_model.h5'):
        """
        Salva o modelo treinado.
        """
        self.model.save(filepath)
        print(f"💾 Modelo salvo em: {filepath}")
    
    def load_model(self, filepath='src/model/saved_models/lstm_model.h5'):
        """
        Carrega um modelo salvo.
        """
        self.model = keras.models.load_model(filepath)
        print(f"📂 Modelo carregado de: {filepath}")
    
    def get_architecture_config(self):
        """
        Retorna a configuração da arquitetura.
        """
        return {
            'sequence_length': self.sequence_length,
            'n_features': self.n_features,
            'total_params': self.model.count_params(),
            'layers': len(self.model.layers)
        }


def create_default_model(sequence_length=24, n_features=13):
    """
    Cria um modelo LSTM com configurações padrão otimizadas.
    """
    model = EnergyLSTMModel(sequence_length, n_features)
    model.build_model(
        lstm_units=[128, 64, 32],
        dropout_rate=0.2
    )
    return model


if __name__ == "__main__":
    # Teste da arquitetura
    print("🧪 Testando arquitetura do modelo...")
    
    model = create_default_model()
    
    # Dados dummy para teste
    X_dummy = np.random.rand(100, 24, 13)
    y_dummy = np.random.rand(100, 1)
    
    print("\n🔍 Testando predição...")
    predictions = model.predict(X_dummy[:5])
    print(f"✅ Shape das predições: {predictions.shape}")
    
    print("\n✅ Teste concluído!")
