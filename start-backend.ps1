# ============================================
# SCRIPT DE START DO BACKEND
# Inicia o servidor FastAPI com auto-reload
# ============================================

Write-Host "🔄 Encerrando processos antigos na porta 8000..." -ForegroundColor Yellow
$processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($processes) {
    foreach ($pid in $processes) {
        Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 1
    Write-Host "✅ Processos encerrados" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Iniciando EnergyFlow AI Backend..." -ForegroundColor Cyan
Write-Host ""

# Ativar ambiente virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    & "venv\Scripts\Activate.ps1"
    Write-Host "✓ Ambiente virtual ativado" -ForegroundColor Green
}

# Iniciar servidor
Write-Host ""
Write-Host "📡 Servidor será iniciado em: http://localhost:8000" -ForegroundColor Yellow
Write-Host "📚 Documentação disponível em: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "🔄 Auto-reload ATIVADO (mudanças são detectadas automaticamente)" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Gray
Write-Host ""

python src\backend\main.py
