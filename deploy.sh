#!/bin/bash

# ==================================
# SCRIPT DE DEPLOY - ENERGYFLOW AI
# ==================================

echo "🚀 EnergyFlow AI - Deploy Script"
echo "================================="
echo ""

# Função para perguntar
ask() {
    read -p "$1 (y/n): " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# 1. Verificar Git
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Instale o Git primeiro."
    exit 1
fi

# 2. Verificar se está em um repositório Git
if [ ! -d .git ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    git add .
    git commit -m "Initial commit - EnergyFlow AI"
else
    echo "✅ Repositório Git encontrado"
fi

# 3. Verificar remote
if ! git remote | grep -q origin; then
    echo ""
    echo "📡 Configure o remote do GitHub:"
    read -p "URL do repositório GitHub: " repo_url
    git remote add origin "$repo_url"
fi

# 4. Push para GitHub
echo ""
if ask "📤 Fazer push para GitHub?"; then
    git add .
    git commit -m "Deploy ready - $(date +%Y-%m-%d)"
    git push -u origin main
    echo "✅ Push concluído!"
fi

# 5. Instruções de Deploy
echo ""
echo "================================="
echo "📋 PRÓXIMOS PASSOS"
echo "================================="
echo ""
echo "Escolha uma plataforma de deploy:"
echo ""
echo "1️⃣  RENDER (RECOMENDADO - Gratuito)"
echo "   👉 https://render.com"
echo "   • New Web Service → Conecte seu repo"
echo "   • Start: uvicorn src.backend.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "2️⃣  RAILWAY (Fácil - Gratuito)"
echo "   👉 https://railway.app"
echo "   • New Project → Deploy from GitHub"
echo "   • Deploy automático!"
echo ""
echo "3️⃣  HEROKU"
echo "   heroku create energyflow-ai"
echo "   git push heroku main"
echo ""
echo "================================="
echo "📚 Documentação completa: DEPLOY_GUIDE.md"
echo "================================="
echo ""
echo "✅ Preparado para deploy!"
