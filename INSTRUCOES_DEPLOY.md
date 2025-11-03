# 🚀 COMO FAZER DEPLOY DO SEU SISTEMA - GUIA PERSONALIZADO

## 📦 O QUE FOI PREPARADO

Seu sistema EnergyFlow AI está 100% pronto para deploy! Foram criados:

✅ **Arquivos de Configuração:**
- `Procfile` - Para Heroku
- `render.yaml` - Para Render (automático)
- `railway.json` - Para Railway
- `vercel.json` - Para Vercel (frontend)
- `Dockerfile` & `docker-compose.yml` - Para Docker
- `.dockerignore` - Otimização Docker

✅ **Scripts de Deploy:**
- `deploy.ps1` - Script PowerShell para Windows
- `deploy.sh` - Script Bash para Linux/Mac

✅ **Documentação:**
- `DEPLOY_GUIDE.md` - Guia completo com todas as opções
- `QUICK_DEPLOY.md` - Guia rápido de 5 minutos
- `DEPLOY_CHECKLIST.md` - Checklist pré-deploy

✅ **Código Atualizado:**
- Frontend detecta automaticamente API em produção
- CORS configurado para aceitar domínios externos
- Health check pronto

---

## 🎯 RECOMENDAÇÃO: USE RENDER (100% GRATUITO)

### Por que Render?
- ✅ Totalmente gratuito (750 horas/mês)
- ✅ HTTPS automático
- ✅ Deploy automático do GitHub
- ✅ Fácil de usar
- ✅ Suporta backend Python + frontend estático

---

## 📝 PASSO A PASSO COMPLETO (15 minutos)

### ETAPA 1: Preparar GitHub (5 min)

1. **Verifique se tem Git instalado:**
   ```powershell
   git --version
   ```

2. **Se não tiver repositório no GitHub:**
   - Vá em https://github.com/new
   - Crie repositório "ia-faculdade"
   - **NÃO** inicialize com README

3. **Configure o repositório local:**
   ```powershell
   cd "c:\Users\Loja Miguel\Documents\MEGA\ia-faculdade"
   
   # Se ainda não iniciou git:
   git init
   
   # Adicione o remote do GitHub:
   git remote add origin https://github.com/SEU-USUARIO/ia-faculdade.git
   
   # Adicione os arquivos:
   git add .
   git commit -m "Sistema pronto para deploy"
   git branch -M main
   git push -u origin main
   ```

   **Substitua SEU-USUARIO pelo seu username do GitHub!**

---

### ETAPA 2: Deploy do Backend no Render (5 min)

1. **Acesse https://render.com**
2. **Faça login com GitHub** (recomendado)
3. Clique em **"New +"** no topo → **"Web Service"**
4. Clique em **"Connect a repository"**
5. Autorize o Render a acessar seus repositórios
6. Selecione o repositório **"ia-faculdade"**
7. Configure:

   ```
   Name: energyflow-api
   Region: Oregon (US West) ou Frankfurt (EU)
   Branch: main
   Root Directory: (deixe vazio)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
   Instance Type: Free
   ```

8. **Adicione variável de ambiente:**
   - Clique em "Advanced"
   - Adicione:
     ```
     Key: PYTHON_VERSION
     Value: 3.10.0
     ```

9. Clique em **"Create Web Service"**
10. **AGUARDE 5-10 minutos** - Render vai instalar tudo
11. Quando terminar, você terá uma URL tipo: `https://energyflow-api.onrender.com`
12. **TESTE**: Acesse `https://energyflow-api.onrender.com/docs` - deve mostrar a documentação da API

---

### ETAPA 3: Deploy do Frontend no Render (3 min)

1. No Render, clique em **"New +"** → **"Static Site"**
2. Selecione o mesmo repositório **"ia-faculdade"**
3. Configure:

   ```
   Name: energyflow-frontend
   Branch: main
   Root Directory: (deixe vazio)
   Build Command: echo "No build needed"
   Publish Directory: src/frontend
   ```

4. Clique em **"Create Static Site"**
5. Aguarde o deploy (1-2 minutos)
6. Você terá uma URL tipo: `https://energyflow-frontend.onrender.com`

---

### ETAPA 4: Conectar Frontend ao Backend (2 min)

1. **Copie a URL do seu backend** (ex: `https://energyflow-api-xyz.onrender.com`)

2. **Atualize o CORS no backend:**
   
   Edite `src/backend/core/config.py`:
   ```python
   CORS_ORIGINS: list = [
       "https://energyflow-frontend.onrender.com",  # ← Sua URL do frontend
       "http://localhost:3000",  # desenvolvimento
       "http://127.0.0.1:3000",
   ]
   ```

3. **Faça commit e push:**
   ```powershell
   git add .
   git commit -m "Adicionar CORS para produção"
   git push
   ```

4. **Render fará redeploy automático!** (2-3 minutos)

5. **PRONTO! 🎉** Acesse sua URL do frontend e teste!

---

## ✅ VERIFICAÇÃO FINAL

### Backend funcionando?
Acesse: `https://SEU-BACKEND.onrender.com/docs`

Você deve ver:
- ✅ Documentação interativa da API
- ✅ Endpoint `/health` retornando status OK
- ✅ Endpoint `/model/info` com informações do modelo

### Frontend funcionando?
Acesse: `https://SEU-FRONTEND.onrender.com`

Você deve ver:
- ✅ Interface do EnergyFlow AI
- ✅ Status da API em verde (conectado)
- ✅ Informações do modelo carregadas
- ✅ Formulário de previsão funcionando

---

## 🐛 PROBLEMAS COMUNS

### 1. "Build failed" no Render
**Solução:** Verifique se `requirements.txt` está no root do projeto

### 2. "Application failed to respond"
**Solução:** Verifique se o comando start está correto:
```
uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
```

### 3. CORS Error no frontend
**Solução:** 
- Verifique se adicionou a URL do frontend em `CORS_ORIGINS`
- Commit e push para atualizar
- Aguarde redeploy (2-3 min)

### 4. "Cannot find module"
**Solução:** Adicione o módulo em `requirements.txt` e faça push

### 5. Frontend não conecta com API
**Solução:** 
- Verifique se backend está rodando (acesse /docs)
- Verifique se CORS está configurado
- Abra DevTools (F12) e veja erros no Console

---

## 🔄 ATUALIZAÇÕES FUTURAS

Sempre que você fizer mudanças no código:

```powershell
cd "c:\Users\Loja Miguel\Documents\MEGA\ia-faculdade"
git add .
git commit -m "Descrição das mudanças"
git push
```

**Render fará deploy automático em 2-3 minutos!** 🚀

---

## 💰 CUSTOS

### Render (Plano Free)
- ✅ Backend: Grátis (750h/mês)
- ✅ Frontend: Grátis (100GB bandwidth)
- ✅ HTTPS: Grátis
- ⚠️ Backend "dorme" após 15min sem uso (acorda em ~30s)

**Total: R$ 0,00/mês** ✅

---

## 📊 ALTERNATIVAS

Se quiser explorar outras opções:

1. **Railway** - Mais rápido, $5 crédito grátis
2. **Heroku** - Tradicional, $7/mês
3. **Vercel** - Só frontend, grátis
4. **DigitalOcean** - VPS, $6/mês, mais controle

Veja detalhes em: `DEPLOY_GUIDE.md`

---

## 🆘 PRECISA DE AJUDA?

1. Leia `DEPLOY_GUIDE.md` - Guia completo com todas as opções
2. Leia `DEPLOY_CHECKLIST.md` - Verifique se não esqueceu nada
3. Verifique logs no Render (aba "Logs")
4. Teste localmente antes:
   ```powershell
   .\venv\Scripts\Activate.ps1
   uvicorn src.backend.main:app --reload
   ```

---

## 🎉 PARABÉNS!

Seu sistema de IA para previsão de energia está agora na web, acessível para qualquer pessoa no mundo! 🌍

**URLs importantes:**
- Backend: `https://energyflow-api-[seu-id].onrender.com`
- Frontend: `https://energyflow-frontend-[seu-id].onrender.com`
- API Docs: `https://energyflow-api-[seu-id].onrender.com/docs`

Compartilhe com o mundo! 🚀
