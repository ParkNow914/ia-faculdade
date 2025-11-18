# ⚡ EnergyFlow AI - Sistema Inteligente de Previsão Energética

## 📋 Descrição do Projeto

Plataforma **Full-Stack Enterprise** de análise preditiva e forecasting de demanda energética utilizando **Machine Learning (Regressão)** com arquitetura de microsserviços moderna e escalável.

### 🎯 Objetivo
Prever consumo de energia elétrica com alta precisão usando algoritmos de regressão ML (Random Forest, Gradient Boosting, Ensemble), permitindo gestão proativa e otimização de recursos energéticos de forma rápida e eficiente.

---

## 🏗️ Arquitetura de Microsserviços

```
┌─────────────────────────────────────────────────┐
│      PRESENTATION LAYER (Web Interface)         │
│  • Dashboard Analytics em tempo real            │
│  • Visualizações interativas (Chart.js)         │
│  • UX/UI Responsivo e moderno                   │
└────────────────┬────────────────────────────────┘
                 │ REST API (JSON)
┌────────────────▼────────────────────────────────┐
│    APPLICATION LAYER (FastAPI Backend)          │
│  • RESTful Endpoints assíncronos                │
│  • Validação Pydantic avançada                  │
│  • Sistema de Cache e otimização                │
│  • Documentação OpenAPI automática              │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│     AI/ML LAYER (Machine Learning Engine)       │
│  • Ensemble Regression Models                   │
│  • Random Forest & Gradient Boosting            │
│  • Feature Engineering Pipeline                 │
│  • Model Serving & Inference                    │
│  • Real-time Prediction Service                 │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico Enterprise

### Backend & API Layer
- **FastAPI** - Framework web async de alta performance
- **Uvicorn** - Servidor ASGI production-ready
- **Pydantic** - Validação de dados com type hints

### AI/ML & Data Science
- **Scikit-learn** - Machine Learning e preprocessing
- **XGBoost** - Gradient Boosting otimizado
- **Pandas** - Data manipulation e análise
- **NumPy** - Computação numérica otimizada
- **Joblib** - Serialização de modelos

### Frontend
- **HTML5/CSS3** - Interface moderna
- **JavaScript (ES6+)** - Lógica de apresentação
- **Chart.js** - Visualização de dados

---

## 📊 Dataset

### ⚠️ IMPORTANTE: Use Dados Reais

O sistema foi projetado para usar **dados reais** de consumo de energia. 

**Datasets Reais Recomendados**:
1. **UCI - Individual Household Electric Power Consumption** ⭐ RECOMENDADO
   - Fonte: UCI Machine Learning Repository
   - Período: 2006-2010 (França)
   - 2+ milhões de medições reais
   - [Como usar](data/README_DADOS_REAIS.md)

2. **Kaggle - Hourly Energy Consumption**
   - Dados de mercado dos EUA
   - Período: 2004-2018

3. **PJM/ERCOT** - Dados de mercado de energia

**Como Obter Dados Reais**:
```bash
# Ver guia completo em:
cat data/README_DADOS_REAIS.md

# Processar dataset UCI (após download):
python data/process_uci_dataset.py
```

⚠️ O arquivo `data/generate_dataset.py` gera dados sintéticos APENAS para testes rápidos. **NÃO use dados sintéticos para trabalhos acadêmicos ou produção.**

---

## 🚀 Instalação e Execução

### 1. Clone o repositório
```bash
cd "PROJETO DE IA-LISSON"
```

### 2. Instale as dependências
```powershell
pip install -r requirements.txt
```

### 3. Obtenha dados reais de energia
```powershell
# Veja instruções detalhadas:
type data\README_DADOS_REAIS.md

# Após obter o dataset UCI, processe:
python data\process_uci_dataset.py
```

### 4. Treine o modelo com dados reais
```powershell
python src\model\train.py
```

### 4. Execute o backend
```powershell
python src/backend/main.py
```

### 5. Abra o frontend
Abra `src/frontend/index.html` no navegador ou execute:
```powershell
python -m http.server 8080 --directory src/frontend
```

---

## 📁 Estrutura do Projeto

```
PROJETO DE IA-LISSON/
├── README.md                    # Documentação principal
├── requirements.txt             # Dependências Python
├── .gitignore                   # Arquivos ignorados
├── docs/                        # Documentação adicional
│   ├── ARCHITECTURE.md          # Arquitetura detalhada
│   └── API.md                   # Documentação da API
├── data/                        # Datasets
│   ├── raw/                     # Dados brutos
│   ├── processed/               # Dados processados
│   └── generate_dataset.py      # Gerador de dados
├── src/
│   ├── model/                   # Camada de IA
│   │   ├── train.py             # Script de treinamento
│   │   ├── model.py             # Arquitetura de Regressão ML
│   │   ├── preprocessing.py     # Pipeline de dados
│   │   └── saved_models/        # Modelos serializados
│   ├── backend/                 # API FastAPI
│   │   ├── main.py              # Entrada da API
│   │   ├── api/
│   │   │   ├── routes.py        # Endpoints
│   │   │   └── schemas.py       # Modelos Pydantic
│   │   ├── core/
│   │   │   ├── config.py        # Configurações
│   │   │   └── predictor.py     # Serviço de previsão
│   │   └── utils/
│   │       └── validators.py    # Validações
│   └── frontend/                # Interface Web
│       ├── index.html           # Página principal
│       ├── css/
│       │   └── style.css        # Estilos
│       └── js/
│           └── app.js           # Lógica do frontend
└── tests/                       # Testes automatizados
    ├── test_model.py
    └── test_api.py
```

---

## 🎓 Conceitos Aplicados (Gestão de T.I.)

### 1. **Machine Learning & Regressão**
- Algoritmos de regressão (Random Forest, Gradient Boosting)
- Ensemble methods
- Feature engineering
- Otimização de hiperparâmetros

### 2. **Arquitetura de Software**
- Separação em camadas
- Microserviços
- API RESTful

### 3. **DevOps & Cloud**
- Containerização (preparado para Docker)
- CI/CD ready
- Deploy em cloud gratuito

### 4. **Qualidade de Software**
- Validação de dados
- Tratamento de erros
- Logging e monitoramento

---

## 📈 Resultados Esperados

- **Acurácia**: Alta precisão com R² > 0.90 (MAE otimizado)
- **Latência**: < 50ms por previsão (mais rápido que redes neurais)
- **Treinamento**: Rápido e eficiente (minutos vs horas)
- **Escalabilidade**: Assíncrono, preparado para concorrência

---

## 📦 Artefatos do Modelo & Render Deploy

- Os arquivos salvos em `src/model/saved_models/` agora são versionados (retirados do `.gitignore`), garantindo que o Render receba o modelo treinado durante o build.
- Sempre que gerar um novo artefato (`regression_model.pkl`, `scaler_features.pkl`, etc.), execute:
  ```
  git add src/model/saved_models/*.pkl
  git commit -m "Atualiza artefatos do modelo"
  git push
  ```
- Opcionalmente, defina a env `MODEL_URL` no Render para baixar automaticamente um artefato hospedado (S3, GDrive, etc.). O build script já suporta `.pkl` ou `.zip`.
- Sem esses arquivos versionados (ou sem `MODEL_URL`), o backend não encontra o modelo e as previsões falham no deploy.

---

## 🌐 Deploy Gratuito (Always Free)

### Opções de Hospedagem:
1. **Backend**: Render.com (Free tier)
2. **Frontend**: Vercel/Netlify
3. **Modelo**: Incluído no backend (serializado)

---

## 👨‍💻 Autor

Projeto desenvolvido para disciplina de IA - Gestão de T.I.

---

## 📄 Licença

MIT License - Livre para uso acadêmico e comercial.

---

## 🔥 Diferenciais do Projeto

✅ **Não é chatbot** - Sistema de previsão real  
✅ **100% treinado** - Modelos de regressão ML otimizados  
✅ **Dataset público** - Dados reais de energia  
✅ **Full-Stack** - Backend + Frontend + IA  
✅ **Enterprise** - Arquitetura profissional  
✅ **Always Free** - Sem custos de infraestrutura  
✅ **Eficiente** - Treinamento rápido e previsões em tempo real  
✅ **Alta Performance** - Machine Learning tradicional mais leve que Deep Learning  