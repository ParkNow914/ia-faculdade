"""
VALIDADORES PERSONALIZADOS
Validações avançadas para dados de entrada.
"""

from typing import Dict, Any, List
from datetime import datetime
import numpy as np

class DataValidator:
    """
    Classe para validações complexas de dados.
    """
    
    @staticmethod
    def validate_prediction_input(data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Valida dados de entrada para previsão.
        
        Returns:
            (is_valid, error_message)
        """
        # Validar temperatura realista
        temp = data.get('temperature_celsius', 0)
        if not -50 <= temp <= 60:
            return False, f"Temperatura {temp}°C fora do range realista (-50 a 60°C)"
        
        # Validar hora
        hour = data.get('hour', 0)
        if not 0 <= hour <= 23:
            return False, f"Hora {hour} inválida (deve ser 0-23)"
        
        # Validar dia da semana
        dow = data.get('day_of_week', 0)
        if not 0 <= dow <= 6:
            return False, f"Dia da semana {dow} inválido (deve ser 0-6)"
        
        # Validar mês
        month = data.get('month', 0)
        if not 1 <= month <= 12:
            return False, f"Mês {month} inválido (deve ser 1-12)"
        
        # Validar consumos históricos (não podem ser negativos)
        for field in ['consumption_lag_1h', 'consumption_lag_24h', 'consumption_lag_168h',
                      'consumption_rolling_mean_24h', 'consumption_rolling_std_24h']:
            value = data.get(field, 0)
            if value < 0:
                return False, f"{field} não pode ser negativo: {value}"
            
            # Validar valores extremos (> 100.000 kWh é suspeito)
            if value > 100000:
                return False, f"{field} com valor suspeito: {value} kWh"
        
        # Validar consistência entre lags
        lag_1h = data.get('consumption_lag_1h', 0)
        lag_24h = data.get('consumption_lag_24h', 0)
        mean_24h = data.get('consumption_rolling_mean_24h', 0)
        
        # Média não pode ser muito diferente dos lags
        if mean_24h > 0:
            if abs(lag_1h - mean_24h) / mean_24h > 3:  # Mais de 3x diferente
                return False, f"Lag 1h ({lag_1h}) muito diferente da média 24h ({mean_24h})"
        
        return True, ""
    
    @staticmethod
    def validate_forecast_hours(hours: int) -> tuple[bool, str]:
        """
        Valida número de horas para forecast.
        """
        if hours < 1:
            return False, "Número de horas deve ser pelo menos 1"
        
        if hours > 168:
            return False, "Número de horas não pode exceder 168 (7 dias)"
        
        return True, ""
    
    @staticmethod
    def detect_anomalies(values: List[float], threshold: float = 3.0) -> List[int]:
        """
        Detecta anomalias em uma série de valores usando z-score.
        
        Args:
            values: Lista de valores
            threshold: Threshold para z-score (padrão: 3.0)
            
        Returns:
            Lista de índices com anomalias
        """
        if len(values) < 3:
            return []
        
        values_array = np.array(values)
        mean = np.mean(values_array)
        std = np.std(values_array)
        
        if std == 0:
            return []
        
        z_scores = np.abs((values_array - mean) / std)
        anomalies = np.where(z_scores > threshold)[0].tolist()
        
        return anomalies
