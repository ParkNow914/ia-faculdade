"""
ENERGYFLOW AI - BACKEND API
Sistema Inteligente de Previsão Energética com Inteligência Artificial Avançada

Otimizado para uso eficiente de memória.
"""

import os
import sys
import gc
import tracemalloc
from pathlib import Path
from typing import Optional

# Configuração inicial para monitoramento de memória
tracemalloc.start()

# Adicionar diretório raiz ao PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from pydantic import BaseModel

from src.backend.core.config import settings
from src.backend.core.logger import setup_logger

# Configurar logger
logger = setup_logger(__name__)

# Importar rotas após configuração do logger
from src.backend.api.routes import router


# === CONFIGURAÇÕES DE MEMÓRIA ===
# Limitar o tamanho máximo de requisição (10MB)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# === CRIAR APLICAÇÃO ===
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG
)


# === MIDDLEWARES ===
@app.middleware("http")
async def limit_body_size(request: Request, call_next):
    """Middleware para limitar o tamanho do corpo da requisição."""
    if request.method in ["POST", "PUT", "PATCH"]:
        content_length = int(request.headers.get("content-length", 0))
        if content_length > MAX_CONTENT_LENGTH:
            return JSONResponse(
                status_code=413,
                content={"error": f"Tamanho da requisição excede o limite de {MAX_CONTENT_LENGTH//(1024*1024)}MB"}
            )
    return await call_next(request)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Apenas métodos necessários
    allow_headers=["*"],
    max_age=600  # Cache de CORS por 10 minutos
)


# === INCLUIR ROTAS ===
app.include_router(router)

# Log das rotas registradas
if settings.DEBUG:
    logger.info(f"📋 {len(router.routes)} rotas registradas")
    for route in router.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            logger.debug(f"   {list(route.methods)} {route.path}")


# === EXCEPTION HANDLERS ===
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global de exceções.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


# === EVENTOS ===
@app.on_event("startup")
async def startup_event():
    """
    Executado ao iniciar a aplicação.
    """
    print("="*80)
    print("ENERGYFLOW AI - BACKEND API")
    print("="*80)
    print(f"Servidor: {settings.HOST}:{settings.PORT}")
    print(f"Documentacao: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Versao: {settings.APP_VERSION}")
    print(f"AI Engine: Scikit-learn + XGBoost (Regressao ML)")
    print("="*80)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado ao encerrar a aplicação.
    """
    print("\n👋 Encerrando EnergyFlow AI...")


# === FUNÇÃO PARA MONITORAR MEMÓRIA ===
def log_memory_usage():
    """Registra o uso de memória atual."""
    if settings.DEBUG:
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        logger.info("\n=== TOP 10 ALOCAÇÕES DE MEMÓRIA ===")
        for stat in top_stats[:10]:
            logger.info(stat)

# === MAIN ===
def main():
    """
    Inicia o servidor Uvicorn com otimizações de memória.
    """
    # Configurações otimizadas para produção
    uvicorn_config = {
        "app": "src.backend.main:app",
        "host": settings.HOST,
        "port": settings.PORT,
        "workers": 1,  # Reduzir workers para economizar memória
        "limit_concurrency": 10,  # Limitar concorrência
        "timeout_keep_alive": 30,  # Encerrar conexões ociosas mais rapidamente
        "log_level": "info",
        "reload": settings.DEBUG,  # Ativar reload apenas em desenvolvimento
        "reload_dirs": ["src"] if settings.DEBUG else None,  # Monitorar mudanças na pasta src
    }
    
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"🔧 Modo {'DESENVOLVIMENTO' if settings.DEBUG else 'PRODUÇÃO'}")
    
    uvicorn.run(**uvicorn_config)


if __name__ == "__main__":
    main()
