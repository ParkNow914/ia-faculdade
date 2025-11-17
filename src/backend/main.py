"""
ENERVISION AI - BACKEND API
Sistema Inteligente de Previsão Energética com Inteligência Artificial Avançada
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime

from src.backend.core.config import settings
from src.backend.api.routes import router
import urllib.request
from pathlib import Path
import os
import zipfile
import shutil


# === CRIAR APLICAÇÃO ===
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)


# === CONFIGURAR CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === INCLUIR ROTAS ===
app.include_router(router)
# Log das rotas registradas (para debug)
print(f"📋 Rotas registradas: {len(router.routes)}")
for route in router.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f"   {list(route.methods)} {route.path}")


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
    print("ENERVISION AI - BACKEND API")
    print("="*80)
    # Tentar garantir que o modelo esteja presente: se não existir e a variável
    # de ambiente MODEL_URL estiver definida, fará o download automático.
    model_path = Path(settings.MODEL_PATH)
    if not model_path.exists():
        model_url = os.environ.get('MODEL_URL') or os.getenv('MODEL_URL')
        if model_url:
            try:
                model_path.parent.mkdir(parents=True, exist_ok=True)
                print(f"🔁 Modelo não encontrado. Baixando de: {model_url}")

                # Baixar para um arquivo temporário
                tmp_file = Path('/tmp') / Path(model_url).name
                urllib.request.urlretrieve(model_url, str(tmp_file))

                # Se for um zip, extrair mantendo estrutura
                if str(tmp_file).lower().endswith('.zip'):
                    try:
                        with zipfile.ZipFile(tmp_file, 'r') as z:
                            z.extractall(path='.')
                        print(f"✅ Arquivo zip extraído no diretório do projeto")
                    except Exception as ze:
                        print(f"⚠️ Falha ao extrair zip: {ze}")
                else:
                    # Salvar diretamente no caminho do modelo
                    shutil.move(str(tmp_file), str(model_path))
                    print(f"✅ Modelo baixado para: {model_path}")

                # Limpar arquivo temporário se ainda existir
                try:
                    if tmp_file.exists():
                        tmp_file.unlink()
                except Exception:
                    pass

            except Exception as e:
                print(f"⚠️ Falha ao baixar ou extrair o modelo: {e}")
        else:
            print(f"[AVISO] Modelo não encontrado em: {settings.MODEL_PATH}")
            print("[INFO] Para deploys automáticos, defina a variável de ambiente MODEL_URL com a URL do artefato do modelo (pode ser .pkl ou .zip com a pasta src/model/saved_models/).")

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
    print("\n👋 Encerrando EnerVision AI...")


# === MAIN ===
def main():
    """
    Inicia o servidor Uvicorn.
    """
    uvicorn.run(
        "src.backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # Sempre ativar reload para desenvolvimento
        reload_dirs=["src"],  # Monitorar mudanças na pasta src
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
