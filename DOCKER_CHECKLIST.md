# ==================================
# CHECKLIST DOCKER - RENDER DEPLOY
# ==================================

## ✅ ARQUIVOS NECESSÁRIOS

- [x] Dockerfile (atualizado e otimizado)
- [x] .dockerignore (otimizado)
- [x] requirements.txt (todas as dependências)
- [x] src/backend/main.py (entry point)
- [x] src/model/saved_models/ (modelo treinado)

## ✅ DOCKERFILE - CARACTERÍSTICAS

- [x] Base: Python 3.10-slim (compatível Render)
- [x] Variável $PORT dinâmica (obrigatório Render)
- [x] Comando: uvicorn (servidor ASGI)
- [x] Health check: /health endpoint
- [x] Usuário não-root (segurança)
- [x] Otimizado para memória limitada (512MB)
- [x] Dependências do sistema incluídas (gcc, g++, libgomp1)

## ✅ COMANDO CORRETO

```dockerfile
CMD uvicorn src.backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

✅ Usa variável $PORT do Render
✅ Fallback para 8000 se não definida

## ✅ HEALTH CHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/health')" || exit 1
```

✅ Verifica endpoint /health
✅ 60s de start period (tempo para carregar modelo ML)

## ✅ ESTRUTURA COPIADA PARA CONTAINER

```
/app/
├── src/
│   ├── backend/
│   │   ├── main.py ✅
│   │   ├── api/
│   │   ├── core/
│   │   └── utils/
│   ├── frontend/ (não usado no backend)
│   └── model/
│       ├── train.py
│       ├── model.py
│       ├── preprocessing.py
│       └── saved_models/
│           ├── regression_model.pkl ✅
│           └── scalers/ ✅
├── data/
│   └── processed/
├── logs/
└── requirements.txt ✅
```

## ✅ OTIMIZAÇÕES PARA RENDER FREE TIER

### Memória (512MB limite)
- [x] Usar Python slim (não full)
- [x] --no-cache-dir no pip install
- [x] Remover apt cache após install
- [x] Copiar apenas arquivos necessários

### Performance
- [x] Layer caching (COPY requirements.txt primeiro)
- [x] Multi-stage build não necessário (modelo pequeno)
- [x] PYTHONUNBUFFERED=1 (logs em tempo real)

## ✅ VARIÁVEIS DE AMBIENTE NO RENDER

Adicione no Render:

```
PORT=8000 (Render define automaticamente)
PYTHON_VERSION=3.10.0 (opcional)
DEBUG=False
LOG_LEVEL=INFO
```

## ✅ TESTE LOCAL ANTES DO DEPLOY

```powershell
# Build
docker build -t energyflow-test .

# Run
docker run -p 8000:8000 -e PORT=8000 energyflow-test

# Testar
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

Ou use o script:
```powershell
.\test-docker.ps1
```

## ✅ CONFIGURAÇÃO NO RENDER

```
Language: Docker ✅
Branch: main
Root Directory: (vazio)
Docker Build Context: .
Dockerfile Path: ./Dockerfile
Instance Type: Free ($0/month) ✅
Health Check Path: /health
Auto-Deploy: On Commit
```

## ⚠️ PROBLEMAS COMUNS

### "Out of memory during build"
- Render Free tem 512MB RAM
- Modelos ML podem usar memória (já otimizado)
- ✅ Solução: Dockerfile já otimizado

### "Application failed to respond"
- ✅ Verificar se $PORT é usado
- ✅ Verificar health check
- ✅ Verificar logs no Render

### "ModuleNotFoundError"
- ✅ Verificar requirements.txt completo
- ✅ Verificar estrutura de pastas

## ✅ PRONTO PARA DEPLOY!

Se todos os itens estão ✅, pode fazer deploy no Render com confiança!

**Comando final de teste:**
```powershell
.\test-docker.ps1
```

Se passar, está 100% pronto! 🚀
