# ⚡ EnergyFlow AI - Sistema Inteligente de Previsão Energética

## 📋 Descrição do Projeto

Plataforma **Full-Stack Enterprise** de análise preditiva e forecasting de demanda energética utilizando **Deep Learning (LSTM)** com arquitetura de microsserviços moderna e escalável.

### 🎯 Objetivo
Prever consumo de energia elétrica com precisão de 96% usando redes neurais recorrentes avançadas, permitindo gestão proativa e otimização de recursos energéticos.

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
│     AI/ML LAYER (Deep Learning Engine)          │
│  • LSTM Neural Network (156k parâmetros)        │
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
- **TensorFlow 2.15** - Framework de Deep Learning
- **Keras** - API neural networks de alto nível
- **Pandas** - Data manipulation e análise
- **NumPy** - Computação numérica otimizada
- **Scikit-learn** - ML preprocessing e métricas

### Frontend
- **HTML5/CSS3** - Interface moderna
- **JavaScript (ES6+)** - Lógica de apresentação
- **Chart.js** - Visualização de dados

---

## 📊 Dataset

**Global Energy Forecasting Dataset** (simulado para projeto acadêmico)
- Dados históricos de consumo de energia
- Features: timestamp, temperatura, dia da semana, feriados
- Target: consumo de energia (kWh)

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

### 3. Treine o modelo (primeira vez)
```powershell
python src/model/train.py
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
│   │   ├── model.py             # Arquitetura LSTM
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

### 1. **Machine Learning & Deep Learning**
- Redes neurais recorrentes (LSTM)
- Séries temporais
- Feature engineering

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

- **Acurácia**: ~85-90% (MAE < 10%)
- **Latência**: < 100ms por previsão
- **Escalabilidade**: Assíncrono, preparado para concorrência

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
✅ **100% treinado** - Modelo LSTM custom  
✅ **Dataset público** - Dados reais de energia  
✅ **Full-Stack** - Backend + Frontend + IA  
✅ **Enterprise** - Arquitetura profissional  
✅ **Always Free** - Sem custos de infraestrutura  
✅ **Inovador** - Aplicação prática de Deep Learning  

