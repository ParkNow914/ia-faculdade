"""
MÉTRICAS E MONITORAMENTO
Sistema de coleta de métricas de performance.
"""

from datetime import datetime
from typing import Dict, List
import time
from collections import defaultdict
import json

class MetricsCollector:
    """
    Coletor de métricas da aplicação.
    """
    
    def __init__(self):
        self.request_count = defaultdict(int)
        self.request_times = defaultdict(list)
        self.errors = []
        self.start_time = datetime.now()
    
    def record_request(self, endpoint: str, duration: float):
        """Registra uma requisição."""
        self.request_count[endpoint] += 1
        self.request_times[endpoint].append(duration)
    
    def record_error(self, endpoint: str, error: str):
        """Registra um erro."""
        self.errors.append({
            'endpoint': endpoint,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_metrics(self) -> Dict:
        """Retorna métricas agregadas."""
        metrics = {
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
            'total_requests': sum(self.request_count.values()),
            'endpoints': {},
            'errors': {
                'count': len(self.errors),
                'recent': self.errors[-10:]  # Últimos 10 erros
            }
        }
        
        # Métricas por endpoint
        for endpoint, times in self.request_times.items():
            if times:
                metrics['endpoints'][endpoint] = {
                    'count': self.request_count[endpoint],
                    'avg_time_ms': sum(times) / len(times) * 1000,
                    'min_time_ms': min(times) * 1000,
                    'max_time_ms': max(times) * 1000
                }
        
        return metrics
    
    def reset(self):
        """Reseta as métricas."""
        self.request_count.clear()
        self.request_times.clear()
        self.errors.clear()


# Instância global
metrics = MetricsCollector()


class PerformanceMonitor:
    """
    Context manager para monitorar performance de operações.
    """
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        metrics.record_request(self.operation_name, duration)
        
        if exc_type is not None:
            metrics.record_error(self.operation_name, str(exc_val))
        
        return False  # Não suprime exceções
