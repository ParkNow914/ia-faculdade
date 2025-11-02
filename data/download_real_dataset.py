"""
DOWNLOAD DE DATASET REAL DE ENERGIA ELÉTRICA
Baixa dados reais de consumo energético de fontes públicas.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

def download_ercot_data():
    """
    Baixa dados reais do ERCOT (Electric Reliability Council of Texas).
    Dataset público de consumo de energia real.
    """
    print("🌐 Baixando dataset real de energia do ERCOT...")
    print("📊 Fonte: https://www.ercot.com/")
    
    try:
        # URL do dataset ERCOT (dados reais públicos)
        # Usando dados históricos de demanda do Texas
        url = "http://www.ercot.com/content/cdr/html/ACTUAL_LOADS_OF_WEATHER_ZONES.csv"
        
        print(f"📥 Baixando de: {url}")
        df = pd.read_csv(url, skiprows=4)
        
        print(f"✅ Dataset baixado! {len(df):,} registros")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao baixar do ERCOT: {e}")
        return None

def download_uci_household_data():
    """
    Baixa dataset UCI Individual Household Electric Power Consumption.
    Dataset real com mais de 2 milhões de medições.
    """
    print("🌐 Baixando dataset real UCI - Household Power Consumption...")
    print("📊 Fonte: UCI Machine Learning Repository")
    
    try:
        # URL do dataset UCI
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip"
        
        print(f"📥 Baixando de: {url}")
        
        # Baixar e extrair
        import urllib.request
        import zipfile
        import io
        
        # Download
        with urllib.request.urlopen(url) as response:
            zip_data = response.read()
        
        # Extrair
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            with zip_file.open('household_power_consumption.txt') as file:
                df = pd.read_csv(file, sep=';', low_memory=False)
        
        print(f"✅ Dataset baixado! {len(df):,} registros")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao baixar UCI: {e}")
        return None

def download_openei_data():
    """
    Baixa dados do OpenEI - Open Energy Information.
    Dados reais de consumo comercial e residencial.
    """
    print("🌐 Baixando dataset real OpenEI...")
    print("📊 Fonte: OpenEI - DOE")
    
    try:
        # URL de exemplo do OpenEI
        # Commercial Building Energy Dataset
        url = "https://openei.org/doe-opendata/dataset/commercial-and-residential-hourly-load-profiles-for-all-tmy3-locations-in-the-united-states/resource/b341f6c6-ab93-4ab9-a760-a8e4b7d6b2e7/download/commercialloadprofiles.csv"
        
        print(f"📥 Baixando de: {url}")
        df = pd.read_csv(url, nrows=50000)  # Limitar para não sobrecarregar
        
        print(f"✅ Dataset baixado! {len(df):,} registros")
        return df
        
    except Exception as e:
        print(f"❌ Erro ao baixar OpenEI: {e}")
        return None

def process_uci_dataset(df):
    """
    Processa o dataset UCI para o formato necessário.
    """
    print("🔧 Processando dataset UCI...")
    
    # Combinar data e hora
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    
    # Remover valores inválidos
    df = df[df['DateTime'].notna()].copy()
    
    # Converter colunas para numérico
    numeric_cols = ['Global_active_power', 'Global_reactive_power', 'Voltage', 
                    'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remover NaNs
    df = df.dropna(subset=numeric_cols)
    
    # Criar dataframe final
    df_final = pd.DataFrame({
        'timestamp': df['DateTime'],
        'consumption_kwh': df['Global_active_power'],  # kW (potência ativa global)
        'voltage': df['Voltage'],
        'intensity': df['Global_intensity'],
        'sub_metering_1': df['Sub_metering_1'],
        'sub_metering_2': df['Sub_metering_2'],
        'sub_metering_3': df['Sub_metering_3']
    })
    
    # Adicionar features temporais
    df_final['hour'] = df_final['timestamp'].dt.hour
    df_final['day_of_week'] = df_final['timestamp'].dt.dayofweek
    df_final['month'] = df_final['timestamp'].dt.month
    df_final['is_weekend'] = (df_final['day_of_week'] >= 5).astype(int)
    
    # Simular temperatura (já que UCI não tem - usar sazonalidade)
    # Temperatura base + variação sazonal + variação diária
    month_temp_base = {1: 10, 2: 12, 3: 15, 4: 18, 5: 22, 6: 26,
                       7: 28, 8: 27, 9: 24, 10: 19, 11: 14, 12: 11}
    
    df_final['temperature_celsius'] = df_final.apply(
        lambda row: month_temp_base[row['month']] + 
                   np.sin((row['hour'] - 6) * np.pi / 12) * 5 +
                   np.random.normal(0, 2),
        axis=1
    )
    
    # Adicionar feriados (simplificado)
    holidays = [(1, 1), (12, 25), (7, 14), (5, 1), (11, 1)]
    df_final['is_holiday'] = df_final.apply(
        lambda row: 1 if (row['timestamp'].month, row['timestamp'].day) in holidays else 0,
        axis=1
    )
    
    # Ordenar por timestamp
    df_final = df_final.sort_values('timestamp').reset_index(drop=True)
    
    print(f"✅ Dataset processado: {len(df_final):,} registros")
    print(f"📅 Período: {df_final['timestamp'].min()} até {df_final['timestamp'].max()}")
    
    return df_final

def save_dataset(df, output_path='data/raw/energy_consumption.csv'):
    """
    Salva o dataset processado.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"💾 Dataset salvo em: {output_path}")
    print(f"\n📈 Estatísticas do consumo:")
    print(df['consumption_kwh'].describe())
    
    print(f"\n📊 Informações do dataset:")
    print(df.info())
    
    return True

def main():
    """
    Função principal para baixar e processar dataset real.
    """
    print("="*80)
    print("📊 DOWNLOAD DE DATASET REAL DE ENERGIA ELÉTRICA")
    print("="*80)
    print()
    
    # Tentar UCI primeiro (mais confiável)
    print("🎯 Tentativa 1: UCI Household Power Consumption Dataset")
    df_raw = download_uci_household_data()
    
    if df_raw is not None:
        # Processar dataset UCI
        df_processed = process_uci_dataset(df_raw)
        
        # Usar apenas os últimos 2 anos de dados
        df_final = df_processed.tail(17520)  # 730 dias * 24 horas
        
        # Salvar
        save_dataset(df_final)
        
        print("\n✅ Dataset real baixado e processado com sucesso!")
        print("📌 Fonte: UCI Machine Learning Repository")
        print("📌 Dataset: Individual Household Electric Power Consumption")
        print("📌 Descrição: Medições reais de consumo elétrico residencial")
        print("📌 Período: 2006-2010 (França)")
        
        return True
    
    print("\n❌ Não foi possível baixar dataset real automaticamente.")
    print("\n💡 INSTRUÇÕES MANUAIS:")
    print("1. Acesse: https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption")
    print("2. Baixe o arquivo 'household_power_consumption.zip'")
    print("3. Extraia e coloque 'household_power_consumption.txt' na pasta data/raw/")
    print("4. Execute: python data/process_uci_manual.py")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
