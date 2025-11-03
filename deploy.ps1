# ==================================
# SCRIPT DE DEPLOY - ENERGYFLOW AI
# PowerShell Version
# ==================================

Write-Host "🚀 EnergyFlow AI - Deploy Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git não encontrado. Instale o Git primeiro." -ForegroundColor Red
    exit 1
}

# 2. Verificar se está em um repositório Git
if (-not (Test-Path .git)) {
    Write-Host "📦 Inicializando repositório Git..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - EnergyFlow AI"
} else {
    Write-Host "✅ Repositório Git encontrado" -ForegroundColor Green
}

# 3. Verificar remote
$hasOrigin = git remote | Select-String -Pattern "origin"
if (-not $hasOrigin) {
    Write-Host ""
    Write-Host "📡 Configure o remote do GitHub:" -ForegroundColor Yellow
    $repoUrl = Read-Host "URL do repositório GitHub"
    git remote add origin $repoUrl
}

# 4. Push para GitHub
Write-Host ""
$push = Read-Host "📤 Fazer push para GitHub? (y/n)"
if ($push -eq "y" -or $push -eq "Y") {
    git add .
    $date = Get-Date -Format "yyyy-MM-dd"
    git commit -m "Deploy ready - $date"
    git push -u origin main
    Write-Host "✅ Push concluído!" -ForegroundColor Green
}

# 5. Instruções de Deploy
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📋 PRÓXIMOS PASSOS" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Escolha uma plataforma de deploy:" -ForegroundColor White
Write-Host ""
Write-Host "1️⃣  RENDER (RECOMENDADO - Gratuito)" -ForegroundColor Green
Write-Host "   👉 https://render.com" -ForegroundColor Yellow
Write-Host "   • New Web Service → Conecte seu repo"
Write-Host "   • Start: uvicorn src.backend.main:app --host 0.0.0.0 --port `$PORT"
Write-Host ""
Write-Host "2️⃣  RAILWAY (Fácil - Gratuito)" -ForegroundColor Green
Write-Host "   👉 https://railway.app" -ForegroundColor Yellow
Write-Host "   • New Project → Deploy from GitHub"
Write-Host "   • Deploy automático!"
Write-Host ""
Write-Host "3️⃣  HEROKU" -ForegroundColor Green
Write-Host "   heroku create energyflow-ai"
Write-Host "   git push heroku main"
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "📚 Documentação completa: DEPLOY_GUIDE.md" -ForegroundColor White
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Preparado para deploy!" -ForegroundColor Green
