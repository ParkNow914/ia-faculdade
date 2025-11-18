# 📡 Documentação da API - EnergyFlow AI

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### 1. Root

**GET** `/`

Informações básicas da API.

**Response:**
```json
{
  "message": "🚀 EnergyFlow AI API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. Health Check

**GET** `/health`

Verifica o status da API e do modelo.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-10-31T14:30:00",
  "model_loaded": true,
  "model_info": {
    "status": "ready",
    "model_path": "src/model/saved_models/regression_model.pkl",
    "model_type": "ensemble",
    "n_estimators": 300,
    "n_base_models": 5,
    "n_features": 13
  }
}
```

---

### 3. Previsão Única

**POST** `/predict`

Faz uma previsão de consumo de energia.

**Request Body:**
```json
{
  "temperature_celsius": 25.5,
  "hour": 14,
  "day_of_week": 2,
  "month": 6,
  "is_weekend": 0,
  "is_holiday": 0,
  "consumption_lag_1h": 5200.0,
  "consumption_lag_24h": 5100.0,
  "consumption_lag_168h": 5050.0,
  "consumption_rolling_mean_24h": 5150.0,
  "consumption_rolling_std_24h": 150.0
}
```

**Parameters:**

| Campo | Tipo | Descrição | Limites |
|-------|------|-----------|---------|
| `temperature_celsius` | float | Temperatura em °C | -50 a 60 |
| `hour` | int | Hora do dia | 0 a 23 |
| `day_of_week` | int | Dia da semana | 0 (Seg) a 6 (Dom) |
| `month` | int | Mês | 1 a 12 |
| `is_weekend` | int | Final de semana | 0 ou 1 |
| `is_holiday` | int | Feriado | 0 ou 1 |
| `consumption_lag_1h` | float | Consumo 1h atrás | ≥ 0 |
| `consumption_lag_24h` | float | Consumo 24h atrás | ≥ 0 |
| `consumption_lag_168h` | float | Consumo 168h atrás | ≥ 0 |
| `consumption_rolling_mean_24h` | float | Média móvel 24h | ≥ 0 |
| `consumption_rolling_std_24h` | float | Desvio padrão 24h | ≥ 0 |

**Response:**
```json
{
  "predicted_consumption_kwh": 5234.56,
  "timestamp": "2024-10-31T14:30:00",
  "confidence": "high"
}
```

**Status Codes:**
- `200`: Sucesso
- `422`: Dados inválidos
- `503`: Modelo não carregado

---

### 4. Previsão em Lote

**POST** `/predict/batch`

Faz múltiplas previsões de uma vez.

**Request Body:**
```json
{
  "data": [
    {
      "temperature_celsius": 25.5,
      "hour": 14,
      ...
    },
    {
      "temperature_celsius": 26.0,
      "hour": 15,
      ...
    }
  ]
}
```

**Limites:**
- Máximo de 100 previsões por requisição

**Response:**
```json
{
  "predictions": [
    {
      "predicted_consumption_kwh": 5234.56,
      "timestamp": "2024-10-31T14:30:00",
      "confidence": "high"
    },
    {
      "predicted_consumption_kwh": 5310.45,
      "timestamp": "2024-10-31T14:30:01",
      "confidence": "high"
    }
  ],
  "total": 2
}
```

---

### 5. Previsão Multi-Hora

**POST** `/forecast`

Prevê o consumo para as próximas N horas.

**Request Body:**
```json
{
  "hours_ahead": 24
}
```

**Parameters:**

| Campo | Tipo | Descrição | Limites |
|-------|------|-----------|---------|
| `hours_ahead` | int | Horas para prever | 1 a 168 |

**Response:**
```json
{
  "forecasts": [
    {
      "timestamp": "2024-10-31T15:00:00",
      "predicted_consumption": 5234.56
    },
    {
      "timestamp": "2024-10-31T16:00:00",
      "predicted_consumption": 5310.45
    }
  ],
  "total_hours": 24,
  "start_time": "2024-10-31T15:00:00",
  "end_time": "2024-11-01T14:00:00"
}
```

---

### 6. Informações do Modelo

**GET** `/model/info`

Retorna informações sobre o modelo carregado.

**Response:**
```json
{
  "status": "ready",
  "model_path": "src/model/saved_models/regression_model.pkl",
  "model_type": "ensemble",
  "n_estimators": 300,
  "n_base_models": 5,
  "n_features": 13
}
```

---

### 7. Estatísticas

**GET** `/stats`

Retorna estatísticas dos dados de treinamento.

**Response:**
```json
{
  "total_records": 17520,
  "consumption": {
    "mean": 5243.67,
    "std": 1023.45,
    "min": 2145.32,
    "max": 8932.10,
    "median": 5200.00
  },
  "temperature": {
    "mean": 22.5,
    "min": 8.2,
    "max": 36.8
  },
  "date_range": {
    "start": "2022-01-01 00:00:00",
    "end": "2023-12-31 23:00:00"
  }
}
```

---

## Tratamento de Erros

### Erro de Validação (422)

```json
{
  "detail": [
    {
      "loc": ["body", "temperature_celsius"],
      "msg": "ensure this value is greater than or equal to -50",
      "type": "value_error"
    }
  ]
}
```

### Erro Interno (500)

```json
{
  "error": "Internal Server Error",
  "detail": "Descrição do erro",
  "timestamp": "2024-10-31T14:30:00"
}
```

### Modelo Não Carregado (503)

```json
{
  "detail": "Modelo não está pronto. Execute o treinamento primeiro."
}
```

---

## Exemplos de Uso

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Previsão
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature_celsius": 25.5,
    "hour": 14,
    "day_of_week": 2,
    "month": 6,
    "is_weekend": 0,
    "is_holiday": 0,
    "consumption_lag_1h": 5200,
    "consumption_lag_24h": 5100,
    "consumption_lag_168h": 5050,
    "consumption_rolling_mean_24h": 5150,
    "consumption_rolling_std_24h": 150
  }'
```

### Python

```python
import requests

url = "http://localhost:8000/predict"
data = {
    "temperature_celsius": 25.5,
    "hour": 14,
    "day_of_week": 2,
    "month": 6,
    "is_weekend": 0,
    "is_holiday": 0,
    "consumption_lag_1h": 5200,
    "consumption_lag_24h": 5100,
    "consumption_lag_168h": 5050,
    "consumption_rolling_mean_24h": 5150,
    "consumption_rolling_std_24h": 150
}

response = requests.post(url, json=data)
print(response.json())
```

### JavaScript (Fetch)

```javascript
const url = 'http://localhost:8000/predict';
const data = {
  temperature_celsius: 25.5,
  hour: 14,
  day_of_week: 2,
  month: 6,
  is_weekend: 0,
  is_holiday: 0,
  consumption_lag_1h: 5200,
  consumption_lag_24h: 5100,
  consumption_lag_168h: 5050,
  consumption_rolling_mean_24h: 5150,
  consumption_rolling_std_24h: 150
};

fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## Documentação Interativa

Acesse a documentação interativa do Swagger UI:

```
http://localhost:8000/docs
```

Ou ReDoc:

```
http://localhost:8000/redoc
```

---

## Rate Limiting

Atualmente sem limitação. Em produção, recomenda-se:
- 100 req/min por IP para `/predict`
- 10 req/min por IP para `/forecast`

---

## CORS

Origins permitidos:
- `http://localhost:8080`
- `http://127.0.0.1:8080`
- `http://localhost:5500`
- `http://127.0.0.1:5500`

---

## Versionamento

Versão atual: **v1.0.0**

Futura implementação de versionamento: `/v1/predict`, `/v2/predict`
