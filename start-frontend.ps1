# ============================================
# SCRIPT DE START DO FRONTEND
# Inicia servidor HTTP para o frontend
# ============================================

Write-Host "🎨 Iniciando Manus-Predictor Frontend..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Frontend será iniciado em: http://localhost:8080" -ForegroundColor Yellow
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Gray
Write-Host ""

python -m http.server 8080 --directory src\frontend
