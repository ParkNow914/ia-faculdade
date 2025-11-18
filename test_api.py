"""
Script de teste para verificar a API
"""

import requests
import json

API_URL = 'http://localhost:8000'

def test_health():
    """Testa o endpoint de saúde"""
    print("🔍 Testando /health...")
    response = requests.get(f'{API_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_model_info():
    """Testa informações do modelo"""
    print("🔍 Testando /model/info...")
    response = requests.get(f'{API_URL}/model/info')
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_forecast():
    """Testa previsão de múltiplas horas"""
    print("🔍 Testando /forecast...")
    data = {"hours_ahead": 24}
    response = requests.post(f'{API_URL}/forecast', json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total de previsões: {result['total_hours']}")
        print(f"Primeira previsão: {result['forecasts'][0]}")
        print(f"Última previsão: {result['forecasts'][-1]}")
    else:
        print(f"Erro: {response.text}")
    print()

if __name__ == '__main__':
    print("=" * 60)
    print("TESTE DA API ENERGYFLOW AI")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_model_info()
        test_forecast()
        print("✅ Todos os testes concluídos!")
    except Exception as e:
        print(f"❌ Erro: {e}")
