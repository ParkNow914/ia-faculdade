"""
SCHEMAS PYDANTIC
Modelos de validação de dados da API.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class PredictionInput(BaseModel):
    """
    Modelo de entrada para previsão única.
    """
    temperature_celsius: float = Field(..., ge=-50, le=60, description="Temperatura em Celsius")
    hour: int = Field(..., ge=0, le=23, description="Hora do dia (0-23)")
    day_of_week: int = Field(..., ge=0, le=6, description="Dia da semana (0=Segunda, 6=Domingo)")
    month: int = Field(..., ge=1, le=12, description="Mês (1-12)")
    is_weekend: int = Field(..., ge=0, le=1, description="Final de semana (0=Não, 1=Sim)")
    is_holiday: int = Field(0, ge=0, le=1, description="Feriado (0=Não, 1=Sim)")
    consumption_lag_1h: float = Field(..., ge=0, description="Consumo 1 hora atrás (kWh)")
    consumption_lag_24h: float = Field(..., ge=0, description="Consumo 24 horas atrás (kWh)")
    consumption_lag_168h: float = Field(..., ge=0, description="Consumo 168 horas atrás (kWh)")
    consumption_rolling_mean_24h: float = Field(..., ge=0, description="Média móvel 24h (kWh)")
    consumption_rolling_std_24h: float = Field(..., ge=0, description="Desvio padrão móvel 24h")
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature_celsius": 25.5,
                "hour": 14,
                "day_of_week": 2,
                "month": 6,
                "is_weekend": 0,
                "is_holiday": 0,
                "consumption_lag_1h": 5200.0,
                "consumption_lag_24h": 5100.0,
                "consumption_lag_168h": 5050.0,
                "consumption_rolling_mean_24h": 5150.0,
                "consumption_rolling_std_24h": 150.0
            }
        }


class PredictionOutput(BaseModel):
    """
    Modelo de saída para previsão.
    """
    predicted_consumption_kwh: float = Field(..., description="Consumo previsto em kWh")
    timestamp: str = Field(..., description="Timestamp da previsão")
    confidence: Optional[str] = Field("high", description="Nível de confiança")
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_consumption_kwh": 5234.56,
                "timestamp": "2024-06-15T14:00:00",
                "confidence": "high"
            }
        }


class BatchPredictionInput(BaseModel):
    """
    Modelo para previsões em lote.
    """
    data: List[PredictionInput] = Field(..., max_length=100, description="Lista de dados para previsão")


class BatchPredictionOutput(BaseModel):
    """
    Modelo de saída para previsões em lote.
    """
    predictions: List[PredictionOutput]
    total: int


class HealthResponse(BaseModel):
    """
    Resposta do health check.
    """
    status: str
    timestamp: str
    model_loaded: bool
    model_info: Optional[dict] = None


class ErrorResponse(BaseModel):
    """
    Resposta de erro padrão.
    """
    error: str
    detail: Optional[str] = None
    timestamp: str


class ForecastRequest(BaseModel):
    """
    Requisição para previsão de múltiplas horas.
    """
    hours_ahead: int = Field(24, ge=1, le=168, description="Horas para prever (1-168)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "hours_ahead": 24
            }
        }


class ForecastOutput(BaseModel):
    """
    Saída de previsão de múltiplas horas.
    """
    forecasts: List[dict]
    total_hours: int
    start_time: str
    end_time: str
