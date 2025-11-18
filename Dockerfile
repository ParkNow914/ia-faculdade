# ==================================
# DOCKERFILE - ENERGYFLOW AI
# Sistema de Previsão de Energia
# Otimizado para Render.com Free Tier
# ==================================

# Estágio de build
FROM python:3.10-slim as builder

# Variáveis de ambiente para build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libgomp1 \
    curl \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar apenas o necessário para instalar dependências
COPY requirements.txt .

# Instalar dependências Python (otimizado para memória limitada)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY src/ ./src/
COPY data/ ./data/

# Criar diretórios necessários
RUN mkdir -p logs data/raw data/processed src/model/saved_models

# Baixar modelo se fornecido
ARG MODEL_URL
RUN if [ -n "${MODEL_URL}" ]; then \
        echo "🔁 MODEL_URL fornecido, tentando baixar..."; \
        mkdir -p src/model/saved_models; \
        TMPFILE="/tmp/$(basename ${MODEL_URL})"; \
        curl -fSL "${MODEL_URL}" -o ${TMPFILE} || (echo "Falha ao baixar MODEL_URL" && exit 0); \
        if echo "${TMPFILE}" | grep -qi \\.zip$ ; then \
            unzip -o ${TMPFILE} -d . || echo "Falha ao extrair zip do modelo"; \
            rm -f ${TMPFILE}; \
        else \
            mv ${TMPFILE} src/model/saved_models/regression_model.pkl || echo "Falha ao mover o modelo"; \
        fi; \
    fi

# Limpar cache e arquivos temporários
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    find /usr/local -type f -name '*.pyc' -delete && \
    find /usr/local -type f -name '*.pyo' -delete

# ==================================
# Estágio final (imagem de produção)
# ==================================
FROM python:3.10-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONPATH=/app

# Instalar apenas dependências de tempo de execução
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copiar do estágio de build
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

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

# Comando otimizado para produção
CMD uvicorn src.backend.main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 1 \
    --limit-concurrency 10 \
    --timeout-keep-alive 30 \
    --no-access-log
