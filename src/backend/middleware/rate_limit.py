"""
MIDDLEWARE PERSONALIZADO - Rate Limiting & Security
Middlewares para segurança e controle de taxa de requisições.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import hashlib


class RateLimiter:
    """
    Rate limiter simples baseado em memória.
    Para produção, use Redis.
    """
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> Tuple[bool, int]:
        """
        Verifica se cliente pode fazer requisição.
        
        Returns:
            (is_allowed, remaining_requests)
        """
        now = time.time()
        minute_ago = now - 60
        
        # Limpar requisições antigas
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]
        
        # Verificar limite
        current_requests = len(self.requests[client_id])
        
        if current_requests >= self.requests_per_minute:
            return False, 0
        
        # Adicionar nova requisição
        self.requests[client_id].append(now)
        
        return True, self.requests_per_minute - current_requests - 1
    
    def reset(self, client_id: str = None):
        """Reseta contador para um cliente ou todos."""
        if client_id:
            self.requests[client_id] = []
        else:
            self.requests.clear()


# Instância global
rate_limiter = RateLimiter(requests_per_minute=100)


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware de rate limiting.
    """
    # Obter identificador do cliente (IP)
    client_ip = request.client.host if request.client else "unknown"
    
    # Verificar se é endpoint que precisa de rate limit
    # Excluir health check e docs
    excluded_paths = ["/health", "/docs", "/redoc", "/openapi.json"]
    
    if request.url.path not in excluded_paths:
        is_allowed, remaining = rate_limiter.is_allowed(client_ip)
        
        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "Rate limit exceeded",
                    "detail": "Too many requests. Please try again in 1 minute.",
                    "retry_after": 60
                },
                headers={"Retry-After": "60"}
            )
        
        # Adicionar headers de rate limit
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    return await call_next(request)


async def request_id_middleware(request: Request, call_next):
    """
    Adiciona ID único a cada requisição para rastreamento.
    """
    # Gerar ID único
    request_id = hashlib.md5(
        f"{time.time()}{request.client.host if request.client else 'unknown'}".encode()
    ).hexdigest()[:16]
    
    # Adicionar ao state da request
    request.state.request_id = request_id
    
    # Processar request
    response = await call_next(request)
    
    # Adicionar header de response
    response.headers["X-Request-ID"] = request_id
    
    return response


async def timing_middleware(request: Request, call_next):
    """
    Mede tempo de processamento de cada request.
    """
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    
    return response
