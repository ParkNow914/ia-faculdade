# 🏗️ Arquitetura do Sistema Manus-Predictor

## Visão Geral

O Manus-Predictor é um sistema **Full-Stack Enterprise** desenvolvido com arquitetura em **três camadas** independentes e escaláveis.

---

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        CAMADA DE APRESENTAÇÃO                   │
│                         (Frontend - SPA)                        │
├─────────────────────────────────────────────────────────────────┤
│  • HTML5/CSS3/JavaScript (ES6+)                                 │
│  • Chart.js para visualizações                                  │
│  • Interface responsiva e moderna                               │
│  • Comunicação via REST API (JSON)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS (REST)
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CAMADA DE APLICAÇÃO                        │
│                    (Backend - FastAPI)                          │
├─────────────────────────────────────────────────────────────────┤
│  • Framework: FastAPI (Async Python)                            │
│  • Servidor: Uvicorn (ASGI)                                     │
│  • Validação: Pydantic Schemas                                  │
│  • CORS configurado para segurança                              │
│  • Endpoints RESTful                                            │
│    - POST /predict (previsão única)                             │
│    - POST /predict/batch (previsões em lote)                    │
│    - POST /forecast (previsão multihora)                        │
│    - GET /health (status do sistema)                            │
│    - GET /model/info (informações do modelo)                    │
│    - GET /stats (estatísticas)                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ In-Memory
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CAMADA DE INTELIGÊNCIA                     │
│               (Machine Learning - Regressão ML)                 │
├─────────────────────────────────────────────────────────────────┤
│  • Framework: Scikit-learn 1.3+ + XGBoost 2.0+                 │
│  • Modelo: Ensemble de Regressão ML                             │
│  • Arquitetura:                                                 │
│    - Random Forest: 300 estimadores, max_depth=25               │
│    - Gradient Boosting: 300 estimadores, max_depth=10           │
│    - XGBoost: 300 estimadores, max_depth=10                     │
│    - Ridge Regression: alpha=0.5                                │
│    - Lasso Regression: alpha=0.05                               │
│    - Meta-learner: StackingRegressor (Ridge)                    │
│  • Preprocessing:                                               │
│    - StandardScaler para normalização                           │
│    - Feature engineering temporal                               │
│    - Seleção de features                                        │
│  • Serialização: Joblib (PKL)                                   │
└─────────────────────────────────────────────────────────────────┘
                         │
                         │ File System
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                      CAMADA DE DADOS                            │
├─────────────────────────────────────────────────────────────────┤
│  • Dataset: CSV (730 dias de dados sintéticos)                  │
│  • Features:                                                    │
│    - Timestamp                                                  │
│    - Temperatura                                                │
│    - Hora do dia (cíclica: sin/cos)                             │
│    - Dia da semana                                              │
│    - Mês (cíclico: sin/cos)                                     │
│    - Final de semana (booleano)                                 │
│    - Feriado (booleano)                                         │
│    - Lags de consumo (1h, 24h, 168h)                            │
│    - Rolling statistics (média, std 24h)                        │
│  • Modelos Salvos:                                              │
│    - regression_model.pkl (modelo treinado)                     │
│    - scaler_features.pkl (scaler de features)                   │
│    - scaler_target.pkl (scaler de target)                       │
│    - model_config.json (configuração)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Fluxo de Dados

### 1. Treinamento (Offline)

```
Dataset CSV → Preprocessing → Feature Engineering → 
Train/Test Split → ML Regression Training → 
Model Serialization → Saved Models
```

### 2. Predição (Online)

```
Frontend (User Input) → FastAPI (Validation) → 
Predictor Service (Load Model) → Preprocessing → 
ML Regression Inference → Denormalization → JSON Response → 
Frontend (Display)
```

---

## Padrões de Projeto Utilizados

### 1. **Singleton Pattern**
- **Onde**: `EnergyPredictor` no backend
- **Por quê**: Carregar o modelo uma única vez na memória

### 2. **Service Layer Pattern**
- **Onde**: `predictor.py`
- **Por quê**: Separar lógica de negócio da API

### 3. **DTO (Data Transfer Object)**
- **Onde**: Pydantic Schemas
- **Por quê**: Validação e serialização automática

### 4. **Pipeline Pattern**
- **Onde**: Preprocessing
- **Por quê**: Sequência de transformações de dados

---

## Escalabilidade

### Horizontal Scaling
- Backend FastAPI é stateless
- Pode ser replicado em múltiplas instâncias
- Load balancer (nginx/traefik) na frente

### Vertical Scaling
- Modelo ML pode ser otimizado (hiperparâmetros, feature selection)
- Cache de predições frequentes (Redis)
- GPU para inferência em larga escala

---

## Segurança

### API
- CORS configurado
- Rate limiting (pode ser adicionado)
- Validação de entrada via Pydantic
- HTTPS em produção

### Modelo
- Modelo serializado sem código executável
- Validação de features na entrada
- Limites de valores aceitáveis

---

## Performance

### Métricas Esperadas
- **Latência de Previsão**: < 100ms
- **Throughput**: 100+ req/s
- **Memória**: ~500MB (modelo carregado)
- **CPU**: ~10% em idle

### Otimizações
- Async/await no backend
- Batch processing
- Model caching
- Feature preprocessing otimizado

---

## Deploy

### Opção 1: Docker (Recomendado)
```dockerfile
# Backend + Modelo em um container
FROM python:3.10-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "src/backend/main.py"]
```

### Opção 2: Serverless
- Backend: Render/Fly.io (Free tier)
- Frontend: Vercel/Netlify
- Modelo: Incluído no backend

---

## Monitoramento

### Logs
- Uvicorn logs automáticos
- Custom logging no backend
- Métricas de predição

### Health Checks
- `/health` endpoint
- Status do modelo
- Uptime monitoring

---

## Evolução Futura

### Fase 2
- [ ] Banco de dados (PostgreSQL)
- [ ] Autenticação JWT
- [ ] API versioning

### Fase 3
- [ ] Retreinamento automático
- [ ] A/B testing de modelos
- [ ] Dashboard analytics

---

## Conclusão

Arquitetura **moderna**, **escalável** e **production-ready** para aplicações de Machine Learning em ambiente enterprise.
