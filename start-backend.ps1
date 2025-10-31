# ============================================
# SCRIPT DE START DO BACKEND
# Inicia o servidor FastAPI
# ============================================

Write-Host "🚀 Iniciando Manus-Predictor Backend..." -ForegroundColor Cyan
Write-Host ""

# Ativar ambiente virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✓ Ambiente virtual ativado" -ForegroundColor Green
}

# Iniciar servidor
Write-Host ""
Write-Host "Servidor será iniciado em: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Documentação disponível em: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Gray
Write-Host ""

python src\backend\main.py
