# ==================================
# DOCKERFILE - ENERGYFLOW AI
# Sistema de Previsão de Energia
# Otimizado para Render.com Free Tier
# ==================================

FROM python:3.10-slim

# Metadados
LABEL maintainer="EnergyFlow AI Team"
LABEL description="Sistema Inteligente de Previsão Energética com Regressão ML"
LABEL version="1.0.0"

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para XGBoost e compilação
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    g++ \
    make \
    libgomp1 \
    curl \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (cache layer)
COPY requirements.txt .

# Instalar dependências Python (otimizado para memória limitada)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY src/ ./src/
COPY data/ ./data/

# Criar diretórios necessários
RUN mkdir -p logs data/raw data/processed src/model/saved_models

# Se o build receber MODEL_URL como build-arg, baixar e extrair durante o build
ARG MODEL_URL
RUN if [ -n "${MODEL_URL}" ]; then \
            echo "🔁 MODEL_URL fornecido, tentando baixar..."; \
            mkdir -p src/model/saved_models; \
            TMPFILE="/tmp/$(basename ${MODEL_URL})"; \
            curl -fSL "${MODEL_URL}" -o ${TMPFILE} || (echo "Falha ao baixar MODEL_URL" && exit 0); \
            if echo "${TMPFILE}" | grep -qi \.zip$ ; then \
                unzip -o ${TMPFILE} -d . || echo "Falha ao extrair zip do modelo"; \
                rm -f ${TMPFILE}; \
            else \
                mv ${TMPFILE} src/model/saved_models/regression_model.pkl || echo "Falha ao mover o modelo para saved_models/regression_model.pkl"; \
            fi; \
        fi

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta (variável dinâmica para Render)
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/health')" || exit 1

# Comando padrão (usa $PORT do Render)
CMD uvicorn src.backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
