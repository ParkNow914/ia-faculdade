# ============================================
# SCRIPT DE INICIALIZAÇÃO RÁPIDA
# Manus-Predictor - Sistema de Previsão de Energia
# ============================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  MANUS-PREDICTOR - INICIALIZAÇÃO RÁPIDA" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Host "[1/6] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python não encontrado! Instale Python 3.8+ primeiro." -ForegroundColor Red
    exit 1
}

# Criar ambiente virtual
Write-Host ""
Write-Host "[2/6] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Ambiente virtual já existe" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  ✓ Ambiente virtual criado" -ForegroundColor Green
}

# Ativar ambiente virtual
Write-Host ""
Write-Host "[3/6] Ativando ambiente virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "  ✓ Ambiente virtual ativado" -ForegroundColor Green

# Instalar dependências
Write-Host ""
Write-Host "[4/6] Instalando dependências..." -ForegroundColor Yellow
Write-Host "  (Isso pode levar alguns minutos...)" -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependências instaladas" -ForegroundColor Green

# Gerar dataset
Write-Host ""
Write-Host "[5/6] Gerando dataset..." -ForegroundColor Yellow
if (Test-Path "data\raw\energy_consumption.csv") {
    Write-Host "  ✓ Dataset já existe" -ForegroundColor Green
} else {
    python data\generate_dataset.py
    Write-Host "  ✓ Dataset gerado" -ForegroundColor Green
}

# Treinar modelo
Write-Host ""
Write-Host "[6/6] Treinando modelo LSTM..." -ForegroundColor Yellow
if (Test-Path "src\model\saved_models\lstm_model.h5") {
    $resposta = Read-Host "  Modelo já existe. Retreinar? (s/N)"
    if ($resposta -eq "s" -or $resposta -eq "S") {
        python src\model\train.py
    } else {
        Write-Host "  ✓ Usando modelo existente" -ForegroundColor Green
    }
} else {
    python src\model\train.py
    Write-Host "  ✓ Modelo treinado" -ForegroundColor Green
}

# Finalização
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  ✅ CONFIGURAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Iniciar o backend:" -ForegroundColor White
Write-Host "     python src\backend\main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Abrir o frontend:" -ForegroundColor White
Write-Host "     python -m http.server 8080 --directory src\frontend" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Acessar no navegador:" -ForegroundColor White
Write-Host "     http://localhost:8080" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. Documentação da API:" -ForegroundColor White
Write-Host "     http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
