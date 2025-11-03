# ⚡ Comandos Rápidos - Deploy

## 🚀 Deploy Completo em 3 Comandos

### 1. Push para GitHub
```powershell
cd "c:\Users\Loja Miguel\Documents\MEGA\ia-faculdade"
git add .
git commit -m "Sistema pronto para deploy"
git push origin main
```

### 2. Abrir Render
```powershell
# Abra no navegador:
start https://render.com
```

### 3. Configurar no Render

**Backend:**
- New Web Service
- Start: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`

**Frontend:**
- New Static Site  
- Publish: `src/frontend`

---

## 🔄 Atualizar Após Deploy

```powershell
# Fazer mudanças no código...

# Commit e push (deploy automático!)
git add .
git commit -m "Atualização"
git push
```

---

## 🧪 Testar Localmente

```powershell
# Backend
.\venv\Scripts\Activate.ps1
uvicorn src.backend.main:app --reload

# Frontend (novo terminal)
python -m http.server 3000 --directory src/frontend
```

---

## 📝 Comandos Git Úteis

```powershell
# Ver status
git status

# Ver histórico
git log --oneline

# Desfazer último commit (manter mudanças)
git reset --soft HEAD~1

# Ver branches
git branch

# Criar nova branch
git checkout -b feature/nova-funcionalidade
```

---

## 🐛 Debug

```powershell
# Ver logs do backend local
uvicorn src.backend.main:app --reload --log-level debug

# Testar health check
Invoke-WebRequest http://localhost:8000/health

# Testar API
Invoke-WebRequest http://localhost:8000/docs
```

---

## 📦 Gerenciar Dependências

```powershell
# Adicionar nova dependência
.\venv\Scripts\Activate.ps1
pip install nome-pacote
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Adicionar dependência: nome-pacote"
git push
```

---

## 🔧 Resetar Ambiente Virtual

```powershell
# Remover venv
Remove-Item -Recurse -Force venv

# Recriar
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🌐 URLs Importantes

Depois do deploy:

- **Backend API**: `https://energyflow-api-[ID].onrender.com`
- **API Docs**: `https://energyflow-api-[ID].onrender.com/docs`
- **Frontend**: `https://energyflow-frontend-[ID].onrender.com`
- **GitHub**: `https://github.com/SEU-USUARIO/ia-faculdade`
- **Render Dashboard**: `https://dashboard.render.com`

---

## ✅ Checklist Rápido

Antes do deploy:
- [ ] Código commitado no GitHub
- [ ] `requirements.txt` atualizado
- [ ] Modelo existe em `src/model/saved_models/`
- [ ] `.env` NÃO está commitado (está no .gitignore)

Depois do deploy:
- [ ] Backend responde em `/health`
- [ ] Documentação abre em `/docs`
- [ ] Frontend carrega corretamente
- [ ] CORS configurado com URL do frontend

---

**Leia mais:** `INSTRUCOES_DEPLOY.md`
