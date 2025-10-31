"""
ROTAS DA API
Endpoints RESTful para o sistema de previsão.
"""

from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import pandas as pd
import os

from src.backend.api.schemas import (
    PredictionInput, PredictionOutput,
    BatchPredictionInput, BatchPredictionOutput,
    HealthResponse, ErrorResponse,
    ForecastRequest, ForecastOutput
)
from src.backend.core.predictor import get_predictor
from src.backend.core.config import settings


# Criar router
router = APIRouter()

# Obter instância do preditor
predictor = get_predictor(settings.MODEL_PATH, settings.SCALER_DIR)


@router.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API.
    """
    return {
        "message": "🚀 Manus-Predictor API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Verifica o status da API e do modelo.
    """
    model_info = predictor.get_model_info() if predictor.is_ready() else None
    
    return HealthResponse(
        status="healthy" if predictor.is_ready() else "model_not_loaded",
        timestamp=datetime.now().isoformat(),
        model_loaded=predictor.is_ready(),
        model_info=model_info
    )


@router.post("/predict", response_model=PredictionOutput, tags=["Prediction"])
async def predict_consumption(data: PredictionInput):
    """
    Faz uma previsão de consumo de energia.
    
    **Parâmetros:**
    - `temperature_celsius`: Temperatura em graus Celsius
    - `hour`: Hora do dia (0-23)
    - `day_of_week`: Dia da semana (0=Segunda, 6=Domingo)
    - `month`: Mês (1-12)
    - `is_weekend`: 0 ou 1
    - `is_holiday`: 0 ou 1
    - `consumption_lag_1h`: Consumo 1 hora atrás
    - `consumption_lag_24h`: Consumo 24 horas atrás
    - `consumption_lag_168h`: Consumo 1 semana atrás
    - `consumption_rolling_mean_24h`: Média móvel 24h
    - `consumption_rolling_std_24h`: Desvio padrão móvel 24h
    
    **Retorna:**
    - Previsão de consumo em kWh
    """
    if not predictor.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não está pronto. Execute o treinamento primeiro."
        )
    
    try:
        # Converter para dict
        input_data = data.model_dump()
        
        # Adicionar timestamp (para compatibilidade)
        input_data['timestamp'] = datetime.now()
        
        # Fazer previsão
        prediction = predictor.predict_single(input_data)
        
        return PredictionOutput(
            predicted_consumption_kwh=prediction,
            timestamp=datetime.now().isoformat(),
            confidence="high"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na previsão: {str(e)}"
        )


@router.post("/predict/batch", response_model=BatchPredictionOutput, tags=["Prediction"])
async def predict_batch(data: BatchPredictionInput):
    """
    Faz previsões em lote.
    
    **Parâmetros:**
    - `data`: Lista de objetos PredictionInput (máx. 100)
    
    **Retorna:**
    - Lista de previsões
    """
    if not predictor.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não está pronto."
        )
    
    try:
        predictions = []
        
        for item in data.data:
            input_data = item.model_dump()
            input_data['timestamp'] = datetime.now()
            
            pred = predictor.predict_single(input_data)
            
            predictions.append(PredictionOutput(
                predicted_consumption_kwh=pred,
                timestamp=datetime.now().isoformat(),
                confidence="high"
            ))
        
        return BatchPredictionOutput(
            predictions=predictions,
            total=len(predictions)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro nas previsões: {str(e)}"
        )


@router.post("/forecast", response_model=ForecastOutput, tags=["Forecast"])
async def forecast_next_hours(request: ForecastRequest):
    """
    Prevê o consumo para as próximas N horas.
    
    **Parâmetros:**
    - `hours_ahead`: Número de horas para prever (1-168)
    
    **Retorna:**
    - Lista de previsões horárias
    
    **Nota:** Requer dados históricos. Em produção, carrega do banco de dados.
    """
    if not predictor.is_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo não está pronto."
        )
    
    try:
        # Carregar dados históricos (demo)
        historical_path = 'data/energy_consumption.csv'
        
        if not os.path.exists(historical_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dados históricos não encontrados. Execute o treinamento primeiro."
            )
        
        df = pd.read_csv(historical_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Usar últimas 1000 linhas
        df_recent = df.tail(1000)
        
        # Fazer previsão
        forecasts = predictor.predict_next_hours(df_recent, hours=request.hours_ahead)
        
        return ForecastOutput(
            forecasts=forecasts,
            total_hours=len(forecasts),
            start_time=forecasts[0]['timestamp'],
            end_time=forecasts[-1]['timestamp']
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na previsão: {str(e)}"
        )


@router.get("/model/info", tags=["Model"])
async def get_model_info():
    """
    Retorna informações sobre o modelo carregado.
    """
    return predictor.get_model_info()


@router.get("/stats", tags=["Statistics"])
async def get_statistics():
    """
    Retorna estatísticas dos dados de treinamento.
    """
    try:
        # Carregar dados
        df = pd.read_csv('data/raw/energy_consumption.csv')
        
        stats = {
            'total_records': len(df),
            'consumption': {
                'mean': float(df['consumption_kwh'].mean()),
                'std': float(df['consumption_kwh'].std()),
                'min': float(df['consumption_kwh'].min()),
                'max': float(df['consumption_kwh'].max()),
                'median': float(df['consumption_kwh'].median())
            },
            'temperature': {
                'mean': float(df['temperature_celsius'].mean()),
                'min': float(df['temperature_celsius'].min()),
                'max': float(df['temperature_celsius'].max())
            },
            'date_range': {
                'start': str(df['timestamp'].min()),
                'end': str(df['timestamp'].max())
            }
        }
        
        return stats
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )
