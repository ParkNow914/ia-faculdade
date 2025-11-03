# 🎨 DEPLOY DO FRONTEND - GUIA RÁPIDO

## ✅ BACKEND JÁ ESTÁ FUNCIONANDO!
- 🌐 **URL:** https://energyflow-api.onrender.com
- 📚 **Docs:** https://energyflow-api.onrender.com/docs
- ✅ **Status:** LIVE e funcional!

---

## 🚀 OPÇÃO 1: DEPLOY NO RENDER (RECOMENDADO)

### 📋 Passo a Passo:

1. **Acesse:** https://dashboard.render.com/

2. **Criar Static Site:**
   - Clique em **"New +"** → **"Static Site"**
   
3. **Conectar Repositório:**
   - Selecione: **ParkNow914/ia-faculdade**
   - Branch: **main**

4. **Configurações:**
   ```yaml
   Name: energyflow-frontend
   Build Command: echo "Static site ready"
   Publish Directory: src/frontend
   ```

5. **Deploy!**
   - Clique em **"Create Static Site"**
   - Aguarde 1-2 minutos ⏱️
   - URL gerada: `https://energyflow-frontend.onrender.com`

### ✅ **PRONTO!** Sistema 100% funcional na web!

---

## 🚀 OPÇÃO 2: VERCEL (ALTERNATIVA RÁPIDA)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy (na raiz do projeto)
vercel --prod

# Quando perguntar:
# - Set up and deploy? Y
# - Which scope? (sua conta)
# - Link to existing project? N
# - What's your project's name? energyflow-frontend
# - In which directory is your code? src/frontend
# - Override settings? N
```

**URL gerada:** `https://energyflow-frontend.vercel.app`

---

## 🚀 OPÇÃO 3: NETLIFY

1. Acesse: https://app.netlify.com/
2. Arraste a pasta `src/frontend` para o site
3. **Ou via CLI:**
   ```bash
   npm i -g netlify-cli
   netlify deploy --prod --dir=src/frontend
   ```

---

## 🧪 TESTAR LOCALMENTE ANTES:

```powershell
# Abrir frontend localmente
cd src/frontend
python -m http.server 3000

# Abrir no navegador:
# http://localhost:3000
```

O frontend já está configurado para conectar automaticamente ao backend em produção!

---

## 📊 URLS FINAIS DO SISTEMA:

| Componente | URL |
|------------|-----|
| 🔧 **Backend API** | https://energyflow-api.onrender.com |
| 📚 **API Docs** | https://energyflow-api.onrender.com/docs |
| 🎨 **Frontend** | `https://energyflow-frontend.onrender.com` (após deploy) |

---

## 🎯 PRÓXIMOS PASSOS:

1. ✅ Backend LIVE → **FEITO!** ✅
2. 🔄 Deploy Frontend → **FAÇA AGORA!** 
3. 🧪 Teste end-to-end → **Após frontend subir**
4. 🎉 Sistema completo na web → **SUCESSO!**

---

## 🆘 PRECISA DE AJUDA?

**Quer que eu faça o deploy do frontend para você?**
Posso criar um script PowerShell para automatizar todo o processo!

Basta me avisar qual opção prefere:
- 🟢 **Render** (gratuito, recomendado)
- 🔵 **Vercel** (rápido e fácil)  
- 🟣 **Netlify** (simples)
