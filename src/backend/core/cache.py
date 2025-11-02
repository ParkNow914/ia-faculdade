"""
SISTEMA DE CACHE
Cache em memória para previsões frequentes.
"""

from typing import Any, Optional
from datetime import datetime, timedelta
import hashlib
import json


class CacheManager:
    """
    Gerenciador de cache simples em memória.
    Para produção, use Redis.
    """
    
    def __init__(self, default_ttl: int = 300):
        """
        Args:
            default_ttl: Tempo de vida padrão em segundos (5 minutos)
        """
        self.cache: dict = {}
        self.default_ttl = default_ttl
    
    def _generate_key(self, data: dict) -> str:
        """
        Gera chave única para os dados.
        """
        # Ordenar dict para garantir mesma chave para mesmos dados
        sorted_data = json.dumps(data, sort_keys=True)
        return hashlib.md5(sorted_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache.
        """
        if key in self.cache:
            value, expiry = self.cache[key]
            
            # Verificar se ainda é válido
            if datetime.now() < expiry:
                return value
            else:
                # Remover se expirado
                del self.cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """
        Armazena valor no cache.
        """
        if ttl is None:
            ttl = self.default_ttl
        
        expiry = datetime.now() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)
    
    def get_or_compute(self, data: dict, compute_fn, ttl: Optional[int] = None) -> Any:
        """
        Obtém do cache ou computa se não existir.
        """
        key = self._generate_key(data)
        
        # Tentar obter do cache
        cached = self.get(key)
        if cached is not None:
            return cached
        
        # Computar
        result = compute_fn()
        
        # Armazenar no cache
        self.set(key, result, ttl)
        
        return result
    
    def clear(self):
        """
        Limpa todo o cache.
        """
        self.cache.clear()
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do cache.
        """
        now = datetime.now()
        valid_entries = sum(1 for _, expiry in self.cache.values() if expiry > now)
        
        return {
            "total_entries": len(self.cache),
            "valid_entries": valid_entries,
            "expired_entries": len(self.cache) - valid_entries
        }


# Instância global
cache = CacheManager(default_ttl=300)  # 5 minutos
