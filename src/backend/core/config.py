"""
CONFIGURAÇÕES DO ENERGYFLOW AI
Centraliza todas as configurações da aplicação.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Configurações da aplicação EnergyFlow AI.
    """
    
    # API
    APP_NAME: str = "EnergyFlow AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Sistema Inteligente de Previsão Energética com Deep Learning"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # Python HTTP Server
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5500",  # Live Server
        "http://127.0.0.1:5500",
        "https://energyflow-frontend.onrender.com",  # Frontend em produção
        "https://energyflow-api.onrender.com",  # Backend em produção
        "*"  # Permitir todas as origens (remova em produção se necessário)
    ]
    
    # Paths
    MODEL_PATH: str = "src/model/saved_models/lstm_model.h5"
    SCALER_DIR: str = "src/model/saved_models"
    
    # Model
    SEQUENCE_LENGTH: int = 24
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True


# Instância global de configurações
settings = Settings()
