# Script para iniciar o backend SEM auto-reload (evita loops infinitos)

Write-Host "🚀 Iniciando Manus-Predictor Backend..." -ForegroundColor Green

# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Iniciar servidor sem reload
Write-Host "📡 Servidor rodando em http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 Documentação em http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "" 
Write-Host "⚠️  Modo SEM auto-reload (evita loops infinitos)" -ForegroundColor Yellow
Write-Host "💡 Pressione Ctrl+C para parar" -ForegroundColor Gray
Write-Host ""

uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --no-reload
