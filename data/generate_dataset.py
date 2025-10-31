"""
GERADOR DE DATASET DE ENERGIA ELÉTRICA
Simula dados realistas de consumo de energia baseado em padrões reais.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_energy_dataset(days=730, output_path='data/raw/energy_consumption.csv'):
    """
    Gera dataset sintético de consumo de energia com padrões realistas.
    
    Args:
        days: Número de dias de dados (730 = 2 anos)
        output_path: Caminho para salvar o dataset
    """
    
    print("🔧 Gerando dataset de energia elétrica...")
    
    # Data inicial
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    
    # Criar timestamps (medições a cada hora)
    timestamps = [start_date + timedelta(hours=i) for i in range(days * 24)]
    
    # Inicializar listas
    consumption = []
    temperature = []
    
    np.random.seed(42)  # Reprodutibilidade
    
    for i, ts in enumerate(timestamps):
        # === PADRÕES TEMPORAIS ===
        hour = ts.hour
        day_of_week = ts.weekday()  # 0 = Segunda, 6 = Domingo
        month = ts.month
        
        # Consumo base (em kWh)
        base_consumption = 5000
        
        # === PADRÃO DIÁRIO ===
        # Pico manhã (7-9h) e noite (18-22h)
        if 7 <= hour <= 9:
            hourly_factor = 1.4
        elif 18 <= hour <= 22:
            hourly_factor = 1.6
        elif 0 <= hour <= 6:
            hourly_factor = 0.6
        else:
            hourly_factor = 1.0
        
        # === PADRÃO SEMANAL ===
        # Fim de semana consome menos
        if day_of_week >= 5:  # Sábado e Domingo
            weekly_factor = 0.75
        else:
            weekly_factor = 1.0
        
        # === PADRÃO SAZONAL ===
        # Verão (Nov-Mar): mais consumo (ar condicionado)
        # Inverno (Jun-Ago): consumo médio (aquecimento)
        if month in [11, 12, 1, 2, 3]:  # Verão
            seasonal_factor = 1.3
            temp_base = 28
            temp_variation = 8
        elif month in [6, 7, 8]:  # Inverno
            seasonal_factor = 1.1
            temp_base = 15
            temp_variation = 6
        else:  # Primavera/Outono
            seasonal_factor = 1.0
            temp_base = 22
            temp_variation = 7
        
        # === TEMPERATURA ===
        # Variação diária de temperatura
        temp_daily = np.sin((hour - 6) * np.pi / 12) * temp_variation
        temp_noise = np.random.normal(0, 2)
        temp = temp_base + temp_daily + temp_noise
        
        # === CONSUMO FINAL ===
        consumption_value = (
            base_consumption * 
            hourly_factor * 
            weekly_factor * 
            seasonal_factor *
            (1 + (temp - 22) * 0.02)  # Correlação com temperatura
        )
        
        # Adicionar ruído realista
        noise = np.random.normal(0, consumption_value * 0.05)
        consumption_value += noise
        
        # Garantir valores positivos
        consumption_value = max(consumption_value, 100)
        
        consumption.append(consumption_value)
        temperature.append(temp)
    
    # === CRIAR DATAFRAME ===
    df = pd.DataFrame({
        'timestamp': timestamps,
        'consumption_kwh': consumption,
        'temperature_celsius': temperature,
        'hour': [ts.hour for ts in timestamps],
        'day_of_week': [ts.weekday() for ts in timestamps],
        'month': [ts.month for ts in timestamps],
        'is_weekend': [1 if ts.weekday() >= 5 else 0 for ts in timestamps],
        'season': [get_season(ts.month) for ts in timestamps]
    })
    
    # === ADICIONAR FERIADOS (simulação simplificada) ===
    # Feriados brasileiros principais
    holidays = [
        (1, 1),   # Ano Novo
        (4, 21),  # Tiradentes
        (5, 1),   # Dia do Trabalho
        (9, 7),   # Independência
        (10, 12), # N. Sra. Aparecida
        (11, 2),  # Finados
        (11, 15), # Proclamação da República
        (12, 25), # Natal
    ]
    
    df['is_holiday'] = df.apply(
        lambda row: 1 if (row['timestamp'].month, row['timestamp'].day) in holidays else 0,
        axis=1
    )
    
    # === SALVAR ===
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset gerado com sucesso!")
    print(f"📊 Total de registros: {len(df):,}")
    print(f"📅 Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    print(f"💾 Salvo em: {output_path}")
    print(f"\n📈 Estatísticas:")
    print(df['consumption_kwh'].describe())
    
    return df


def get_season(month):
    """Retorna a estação do ano baseado no mês (Hemisfério Sul)"""
    if month in [12, 1, 2]:
        return 'summer'
    elif month in [3, 4, 5]:
        return 'autumn'
    elif month in [6, 7, 8]:
        return 'winter'
    else:
        return 'spring'


if __name__ == "__main__":
    # Gerar dataset
    df = generate_energy_dataset(days=730)
    
    print("\n🔍 Primeiras linhas do dataset:")
    print(df.head(10))
    
    print("\n📊 Informações do dataset:")
    print(df.info())
