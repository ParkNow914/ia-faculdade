# ==================================
# TESTE DOCKER LOCALMENTE
# ==================================

Write-Host "🐳 Testando Docker localmente..." -ForegroundColor Cyan
Write-Host ""

# Verificar se Docker está instalado
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker não está instalado!" -ForegroundColor Red
    Write-Host "Instale: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Docker encontrado" -ForegroundColor Green

# Parar containers existentes
Write-Host "`n🛑 Parando containers antigos..." -ForegroundColor Yellow
docker stop energyflow-test 2>$null
docker rm energyflow-test 2>$null

# Build da imagem
Write-Host "`n🔨 Building imagem Docker..." -ForegroundColor Cyan
docker build -t energyflow-ai:test .

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Erro no build!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Build concluído!" -ForegroundColor Green

# Rodar container
Write-Host "`n🚀 Iniciando container..." -ForegroundColor Cyan
docker run -d `
    --name energyflow-test `
    -p 8000:8000 `
    -e PORT=8000 `
    -e DEBUG=False `
    energyflow-ai:test

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Erro ao iniciar container!" -ForegroundColor Red
    exit 1
}

Write-Host "`n✅ Container iniciado!" -ForegroundColor Green
Write-Host "`n⏳ Aguardando servidor iniciar (30 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Testar health
Write-Host "`n🏥 Testando health check..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Health check OK!" -ForegroundColor Green
        Write-Host $response.Content
    }
} catch {
    Write-Host "❌ Health check falhou!" -ForegroundColor Red
    Write-Host "`n📋 Logs do container:" -ForegroundColor Yellow
    docker logs energyflow-test
    exit 1
}

# Testar API docs
Write-Host "`n📚 Testando documentação..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Documentação OK!" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️ Documentação não acessível" -ForegroundColor Yellow
}

# Mostrar logs
Write-Host "`n📋 Últimas linhas dos logs:" -ForegroundColor Cyan
docker logs --tail 20 energyflow-test

Write-Host "`n" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ DOCKER FUNCIONANDO PERFEITAMENTE!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "`n🌐 Acesse:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/health" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "`n📊 Comandos úteis:" -ForegroundColor Cyan
Write-Host "  Ver logs:    docker logs -f energyflow-test"
Write-Host "  Parar:       docker stop energyflow-test"
Write-Host "  Remover:     docker rm energyflow-test"
Write-Host "`n🚀 Pronto para deploy no Render!" -ForegroundColor Green
Write-Host ""
