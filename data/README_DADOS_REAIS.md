# 📊 GUIA PARA USO DE DADOS REAIS DE ENERGIA

## ⚠️ IMPORTANTE: Dataset Sintético vs Real

O sistema **atualmente utiliza dados sintéticos** gerados pelo script `generate_dataset.py`. Para usar dados REAIS de consumo de energia, siga um dos métodos abaixo.

---

## 🎯 DATASETS REAIS RECOMENDADOS

### 1. UCI - Individual Household Electric Power Consumption ⭐ RECOMENDADO

**Descrição**: Medições reais de consumo elétrico residencial de uma casa na França  
**Período**: Dezembro 2006 - Novembro 2010 (47 meses)  
**Granularidade**: Medições a cada minuto  
**Tamanho**: 2.075.259 registros  
**Formato**: CSV/TXT

**Como obter**:
```bash
# Método 1: Download direto
wget https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip
unzip household_power_consumption.zip
mv household_power_consumption.txt data/raw/

# Método 2: Download manual
# 1. Acesse: https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption
# 2. Clique em "Data Folder"
# 3. Baixe "household_power_consumption.zip"
# 4. Extraia e coloque o arquivo .txt em data/raw/
```

**Processar dados**:
```bash
python data/process_uci_dataset.py
```

**Features disponíveis**:
- `Global_active_power`: Potência ativa global (kW)
- `Global_reactive_power`: Potência reativa global (kW)
- `Voltage`: Voltagem (V)
- `Global_intensity`: Intensidade de corrente global (A)
- `Sub_metering_1`: Cozinha (Wh)
- `Sub_metering_2`: Lavanderia (Wh)
- `Sub_metering_3`: Aquecedor/ar-condicionado (Wh)

---

### 2. Kaggle - Hourly Energy Consumption

**Descrição**: Consumo energético horário de regiões dos EUA  
**Período**: 2004-2018  
**Granularidade**: Horária  

**Como obter**:
```bash
# Requer Kaggle API instalada
pip install kaggle

# Configure suas credenciais Kaggle em ~/.kaggle/kaggle.json

# Baixar dataset
kaggle datasets download -d robikscube/hourly-energy-consumption
unzip hourly-energy-consumption.zip -d data/raw/
```

**Link**: https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption

---

### 3. PJM Hourly Energy Consumption

**Descrição**: Dados de consumo do PJM Interconnection (maior mercado de energia dos EUA)  
**Período**: 2002-2018  
**Regiões**: Múltiplas (AEP, COMED, DAYTON, DEOK, DOM, DUQ, EKPC, etc.)  

**Como obter**:
```bash
# Via Kaggle
kaggle datasets download -d robikscube/hourly-energy-consumption
```

---

### 4. London Smart Meters

**Descrição**: Dados de medidores inteligentes de Londres  
**Período**: 2011-2014  
**Residências**: 5.567 casas  

**Link**: https://data.london.gov.uk/dataset/smartmeter-energy-use-data-in-london-households

---

### 5. ERCOT (Electric Reliability Council of Texas)

**Descrição**: Dados de demanda de energia do Texas  
**Atualização**: Dados em tempo real disponíveis  

**Link**: http://www.ercot.com/gridinfo/load/load_hist/

---

## 🔄 PROCESSO DE CONVERSÃO PARA O SISTEMA

Independente do dataset escolhido, você precisa convertê-lo para o formato esperado pelo sistema:

### Formato Esperado

O arquivo `data/raw/energy_consumption.csv` deve ter as seguintes colunas:

```csv
timestamp,consumption_kwh,temperature_celsius,hour,day_of_week,month,is_weekend,is_holiday
2022-01-01 00:00:00,5234.5,22.5,0,5,1,1,1
2022-01-01 01:00:00,4891.2,21.8,1,5,1,1,1
...
```

**Colunas obrigatórias**:
- `timestamp`: Data e hora (formato: YYYY-MM-DD HH:MM:SS)
- `consumption_kwh`: Consumo em kWh (ou potência em kW)
- `temperature_celsius`: Temperatura em graus Celsius
- `hour`: Hora do dia (0-23)
- `day_of_week`: Dia da semana (0=Segunda, 6=Domingo)
- `month`: Mês (1-12)
- `is_weekend`: Flag de fim de semana (0 ou 1)
- `is_holiday`: Flag de feriado (0 ou 1)

---

## 📝 SCRIPT DE CONVERSÃO PERSONALIZADO

Se você tem um dataset diferente, crie um script de conversão:

```python
import pandas as pd
import numpy as np

# Carregar seu dataset
df = pd.read_csv('seu_dataset.csv')

# Converter para formato esperado
df_converted = pd.DataFrame({
    'timestamp': pd.to_datetime(df['sua_coluna_data']),
    'consumption_kwh': df['sua_coluna_consumo'],
    'temperature_celsius': df['sua_coluna_temp'],  # ou simular se não tiver
})

# Adicionar features temporais
df_converted['hour'] = df_converted['timestamp'].dt.hour
df_converted['day_of_week'] = df_converted['timestamp'].dt.dayofweek
df_converted['month'] = df_converted['timestamp'].dt.month
df_converted['is_weekend'] = (df_converted['day_of_week'] >= 5).astype(int)
df_converted['is_holiday'] = 0  # Adicionar lógica de feriados se necessário

# Salvar
df_converted.to_csv('data/raw/energy_consumption.csv', index=False)
```

---

## 🛠️ SCRIPTS PRONTOS

### Script para UCI Dataset

Arquivo: `data/process_uci_dataset.py`

```bash
python data/process_uci_dataset.py
```

### Script para Kaggle Hourly Energy

Arquivo: `data/process_kaggle_hourly.py`

```bash
python data/process_kaggle_hourly.py
```

---

## ✅ VERIFICAÇÃO

Após converter seus dados, verifique se está no formato correto:

```python
import pandas as pd

df = pd.read_csv('data/raw/energy_consumption.csv')

# Verificar colunas
print("Colunas:", df.columns.tolist())

# Verificar tipos
print("\nTipos:")
print(df.dtypes)

# Verificar primeiras linhas
print("\nPrimeiras linhas:")
print(df.head())

# Verificar estatísticas
print("\nEstatísticas:")
print(df['consumption_kwh'].describe())

# Verificar período
print(f"\nPeríodo: {df['timestamp'].min()} até {df['timestamp'].max()}")
print(f"Total de registros: {len(df):,}")
```

---

## 🚀 TREINAR MODELO COM DADOS REAIS

Após configurar o dataset real:

```bash
# 1. Verificar se o dataset está correto
python -c "import pandas as pd; df = pd.read_csv('data/raw/energy_consumption.csv'); print(df.info())"

# 2. Treinar modelo
python src/model/train.py

# 3. Iniciar backend
python src/backend/main.py

# 4. Iniciar frontend
python -m http.server 8080 --directory src/frontend
```

---

## 📌 RECOMENDAÇÕES

### Para Projeto Acadêmico
- **UCI Dataset**: Melhor opção - dados reais, bem documentados, aceito academicamente
- Cite a fonte nos seus trabalhos

### Para Projeto Profissional
- **PJM ou ERCOT**: Dados de mercado real de energia
- Maior escala e relevância comercial

### Para Prototipagem Rápida
- **London Smart Meters**: Múltiplas residências, bom para comparações
- Dados já limpos e estruturados

---

## 📚 CITAÇÕES

Se usar datasets públicos, cite corretamente:

**UCI Dataset**:
```
Hebrail, Georges and Berard, Alice. (2012). Individual household electric power consumption. 
UCI Machine Learning Repository. https://doi.org/10.24432/C58K54
```

**Para uso em apresentações/trabalhos**:
- Mencione a fonte do dataset
- Link para o dataset original
- Período dos dados
- Número de registros

---

## ⚠️ IMPORTANTE

1. **Dados Sintéticos NÃO são adequados** para trabalhos acadêmicos sérios
2. **Sempre use dados reais** quando possível
3. **Cite as fontes** corretamente
4. **Verifique a licença** do dataset antes de usar

---

## 🆘 PRECISA DE AJUDA?

Se tiver dificuldades para obter ou processar dados reais:

1. Verifique se o dataset está acessível
2. Confira se as colunas estão no formato correto
3. Valide se não há valores faltantes críticos
4. Teste com um subset pequeno primeiro (1000 linhas)

---

## 📞 CONTATO

Para dúvidas sobre qual dataset usar ou como processar:
- Abra uma issue no GitHub
- Consulte a documentação do dataset escolhido
- Verifique exemplos em Kaggle Notebooks

---

**Última atualização**: Novembro 2024
