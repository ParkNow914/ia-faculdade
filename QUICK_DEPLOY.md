# 🚀 Deploy Rápido - 5 Minutos

## Opção 1: Render (100% Gratuito)

### Backend (API)
1. Acesse [render.com](https://render.com) e faça login com GitHub
2. Clique **"New +"** → **"Web Service"**
3. Conecte este repositório
4. Configure:
   - **Start Command**: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: `PYTHON_VERSION=3.10.0`
5. Deploy! ✅

### Frontend
1. No Render, **"New +"** → **"Static Site"**
2. Conecte o repositório
3. Configure:
   - **Publish Directory**: `src/frontend`
4. Deploy! ✅

### Conectar Frontend ao Backend
1. Copie a URL do backend (ex: `https://energyflow-api.onrender.com`)
2. Adicione no CORS do backend (`src/backend/core/config.py`):
```python
CORS_ORIGINS: list = [
    "https://seu-frontend.onrender.com",
    ...
]
```
3. Commit e push - Render faz redeploy automático!

---

## Opção 2: Railway (1-Click Deploy)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Clique no botão acima
2. Conecte com GitHub
3. Selecione este repositório
4. Deploy automático! ✅

---

## Verificar Deploy

Acesse: `https://sua-api.onrender.com/docs`

Se ver a documentação da API, está funcionando! 🎉

---

## Problemas?

Veja o guia completo: [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
