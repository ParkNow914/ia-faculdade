"""
PROCESSADOR DE DATASET UCI - HOUSEHOLD POWER CONSUMPTION
Converte o dataset UCI para o formato necessário pelo sistema.

Dataset: Individual Household Electric Power Consumption
Fonte: UCI Machine Learning Repository
URL: https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def process_uci_dataset(input_path='data/raw/household_power_consumption.txt', 
                        output_path='data/raw/energy_consumption.csv',
                        num_days=None):
    """
    Processa o dataset UCI para o formato necessário.
    
    Args:
        input_path: Caminho para o arquivo UCI baixado
        output_path: Caminho para salvar o dataset processado
        num_days: Número de dias para usar (None = TODOS os dados disponíveis)
    """
    
    print("="*80)
    print("📊 PROCESSAMENTO DE DATASET REAL UCI")
    print("="*80)
    print()
    
    # Verificar se arquivo existe
    if not os.path.exists(input_path):
        print(f"❌ Arquivo não encontrado: {input_path}")
        print()
        print("📥 COMO OBTER O DATASET:")
        print("1. Acesse: https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption")
        print("2. Baixe 'household_power_consumption.zip'")
        print("3. Extraia e coloque 'household_power_consumption.txt' em data/raw/")
        print()
        return False
    
    print(f"📂 Carregando dataset de: {input_path}")
    
    # Carregar dataset
    df = pd.read_csv(input_path, sep=';', low_memory=False, 
                     parse_dates={'DateTime': ['Date', 'Time']},
                     dayfirst=True)
    
    print(f"✅ Dataset carregado: {len(df):,} registros")
    print(f"📅 Período: {df['DateTime'].min()} até {df['DateTime'].max()}")
    print()
    
    # Converter colunas para numérico
    print("🔧 Convertendo colunas para numérico...")
    numeric_cols = ['Global_active_power', 'Global_reactive_power', 'Voltage', 
                    'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remover linhas com valores faltantes
    df_clean = df.dropna()
    print(f"✅ Após limpeza: {len(df_clean):,} registros ({len(df_clean)/len(df)*100:.1f}%)")
    print()
    
    # Agregar para dados horários (o UCI tem dados por minuto)
    print("⏰ Agregando para dados horários...")
    df_clean['timestamp'] = df_clean['DateTime'].dt.floor('H')
    
    df_hourly = df_clean.groupby('timestamp').agg({
        'Global_active_power': 'mean',  # kW médio na hora
        'Voltage': 'mean',
        'Global_intensity': 'mean',
        'Sub_metering_1': 'sum',  # Wh total na hora
        'Sub_metering_2': 'sum',
        'Sub_metering_3': 'sum'
    }).reset_index()
    
    print(f"✅ Dados horários: {len(df_hourly):,} registros")
    print()
    
    # Selecionar dados (todos ou últimos N dias)
    if num_days is None:
        df_final = df_hourly.copy()
        print(f"📊 Usando TODOS os dados disponíveis: {len(df_final):,} horas")
    else:
        num_hours = num_days * 24
        df_final = df_hourly.tail(num_hours).copy()
        print(f"📊 Selecionando últimos {num_days} dias ({num_hours:,} horas)...")
    print()
    
    # Renomear coluna principal
    df_final = df_final.rename(columns={'Global_active_power': 'consumption_kwh'})
    
    # Adicionar features temporais
    print("🔧 Adicionando features temporais...")
    df_final['hour'] = df_final['timestamp'].dt.hour
    df_final['day_of_week'] = df_final['timestamp'].dt.dayofweek
    df_final['month'] = df_final['timestamp'].dt.month
    df_final['is_weekend'] = (df_final['day_of_week'] >= 5).astype(int)
    
    # Adicionar temperatura simulada baseada em sazonalidade
    # (O dataset UCI não inclui temperatura, então simulamos de forma realista)
    print("🌡️ Simulando temperatura baseada em sazonalidade...")
    
    # Temperatura base por mês (França - hemisfério norte)
    month_temp_base = {
        1: 4,   # Janeiro - inverno
        2: 6,   # Fevereiro
        3: 10,  # Março - primavera
        4: 13,  # Abril
        5: 17,  # Maio
        6: 20,  # Junho - verão
        7: 22,  # Julho
        8: 22,  # Agosto
        9: 18,  # Setembro - outono
        10: 14, # Outubro
        11: 9,  # Novembro
        12: 5   # Dezembro - inverno
    }
    
    def calculate_temperature(row):
        # Temperatura base do mês
        base_temp = month_temp_base[row['month']]
        
        # Variação diária (mais quente à tarde)
        daily_variation = np.sin((row['hour'] - 6) * np.pi / 12) * 4
        
        # Ruído realista
        noise = np.random.normal(0, 2)
        
        return base_temp + daily_variation + noise
    
    df_final['temperature_celsius'] = df_final.apply(calculate_temperature, axis=1)
    
    # Adicionar feriados franceses principais
    print("📅 Adicionando feriados...")
    french_holidays = [
        (1, 1),   # Ano Novo
        (5, 1),   # Dia do Trabalho
        (7, 14),  # Dia da Bastilha
        (8, 15),  # Assunção
        (11, 1),  # Dia de Todos os Santos
        (11, 11), # Armistício
        (12, 25)  # Natal
    ]
    
    df_final['is_holiday'] = df_final.apply(
        lambda row: 1 if (row['timestamp'].month, row['timestamp'].day) in french_holidays else 0,
        axis=1
    )
    
    # Reordenar colunas
    columns_order = [
        'timestamp', 'consumption_kwh', 'temperature_celsius',
        'hour', 'day_of_week', 'month', 'is_weekend', 'is_holiday',
        'Voltage', 'Global_intensity', 
        'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'
    ]
    
    df_final = df_final[columns_order]
    
    # Salvar
    print("💾 Salvando dataset processado...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False)
    
    print()
    print("="*80)
    print("✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print()
    print(f"📁 Arquivo salvo: {output_path}")
    print(f"📊 Total de registros: {len(df_final):,}")
    print(f"📅 Período: {df_final['timestamp'].min()} até {df_final['timestamp'].max()}")
    print()
    print("📈 Estatísticas de consumo (kWh):")
    print(df_final['consumption_kwh'].describe())
    print()
    print("📌 DATASET REAL PRONTO PARA USO!")
    print("📌 Fonte: UCI Machine Learning Repository")
    print("📌 Dados: Individual Household Electric Power Consumption (França, 2006-2010)")
    print()
    print("🚀 Próximos passos:")
    print("  1. python src/model/train.py          # Treinar modelo com dados reais")
    print("  2. python src/backend/main.py         # Iniciar backend")
    print("  3. Acesse http://localhost:8000/docs  # Testar API")
    print()
    
    return True

if __name__ == "__main__":
    success = process_uci_dataset()
    
    if not success:
        print("⚠️ Execute o download manual conforme instruções acima.")
        exit(1)
