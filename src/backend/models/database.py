"""
MODELOS DE BANCO DE DADOS (SQLAlchemy)
Preparado para integração futura com PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Prediction(Base):
    """
    Modelo para armazenar histórico de previsões.
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(16), unique=True, index=True)
    
    # Inputs
    temperature_celsius = Column(Float)
    hour = Column(Integer)
    day_of_week = Column(Integer)
    month = Column(Integer)
    is_weekend = Column(Boolean)
    is_holiday = Column(Boolean)
    
    # Historical features
    consumption_lag_1h = Column(Float)
    consumption_lag_24h = Column(Float)
    consumption_lag_168h = Column(Float)
    consumption_rolling_mean_24h = Column(Float)
    consumption_rolling_std_24h = Column(Float)
    
    # Output
    predicted_consumption_kwh = Column(Float)
    confidence = Column(String(20))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    model_version = Column(String(50))
    processing_time_ms = Column(Float)
    
    def __repr__(self):
        return f"<Prediction(id={self.id}, consumption={self.predicted_consumption_kwh:.2f} kWh)>"


class ModelMetrics(Base):
    """
    Modelo para armazenar métricas do modelo.
    """
    __tablename__ = "model_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    model_version = Column(String(50), index=True)
    
    # Training metrics
    mae = Column(Float)
    rmse = Column(Float)
    r2_score = Column(Float)
    mape = Column(Float)
    
    # Model info
    total_params = Column(Integer)
    training_samples = Column(Integer)
    validation_samples = Column(Integer)
    
    # Timestamps
    trained_at = Column(DateTime, default=datetime.utcnow)
    
    # Config
    config_json = Column(Text)  # JSON string com configurações
    
    def __repr__(self):
        return f"<ModelMetrics(version={self.model_version}, r2={self.r2_score:.4f})>"


class APILog(Base):
    """
    Modelo para logs de API.
    """
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(16), index=True)
    
    endpoint = Column(String(255), index=True)
    method = Column(String(10))
    
    status_code = Column(Integer, index=True)
    processing_time_ms = Column(Float)
    
    client_ip = Column(String(45))
    user_agent = Column(String(255))
    
    # Request/Response
    request_body = Column(Text, nullable=True)
    response_body = Column(Text, nullable=True)
    
    # Error info
    error_message = Column(Text, nullable=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<APILog(endpoint={self.endpoint}, status={self.status_code})>"


class DatasetInfo(Base):
    """
    Informações sobre datasets utilizados.
    """
    __tablename__ = "dataset_info"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), unique=True)
    source = Column(String(255))
    
    total_records = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Statistics
    consumption_mean = Column(Float)
    consumption_std = Column(Float)
    consumption_min = Column(Float)
    consumption_max = Column(Float)
    
    # Metadata
    file_path = Column(String(500))
    file_size_mb = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<DatasetInfo(name={self.name}, records={self.total_records})>"


# Funções auxiliares
def create_db_engine(database_url: str):
    """Cria engine do SQLAlchemy."""
    return create_engine(database_url, echo=False)


def create_tables(engine):
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)


def get_session(engine):
    """Retorna uma sessão do banco de dados."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
