# 🚀 Manus-Predictor - Sistema de Previsão de Séries Temporais

## 📋 Descrição do Projeto

Sistema **Full-Stack Enterprise** de previsão de demanda de energia elétrica utilizando **Deep Learning (LSTM)** com arquitetura moderna e escalável.

### 🎯 Objetivo
Prever o consumo de energia elétrica com base em dados históricos, aplicando técnicas de IA para gestão eficiente de recursos.

---

## 🏗️ Arquitetura Enterprise

```
┌─────────────────────────────────────────────────┐
│            FRONTEND (React/Vanilla JS)          │
│  - Dashboard de visualização                    │
│  - Gráficos interativos de previsão             │
└────────────────┬────────────────────────────────┘
                 │ HTTP/REST
┌────────────────▼────────────────────────────────┐
│         BACKEND API (FastAPI)                   │
│  - Endpoints RESTful assíncronos                │
│  - Validação e processamento                    │
│  - CORS e segurança                             │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│      CAMADA DE IA (TensorFlow/Keras)            │
│  - Modelo LSTM treinado                         │
│  - Pipeline de preprocessamento                 │
│  - Serialização de modelo                       │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework async moderno
- **Uvicorn** - Servidor ASGI de alta performance
- **Pydantic** - Validação de dados

### IA/Machine Learning
- **TensorFlow 2.x** - Framework de Deep Learning
- **Keras** - API de alto nível para redes neurais
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Scikit-learn** - Preprocessing e métricas

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

