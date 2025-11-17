# ✅ Checklist Pré-Deploy

## Antes de fazer deploy, verifique:

### 1. Repositório Git
- [ ] Código está no GitHub
- [ ] Branch main está atualizada
- [ ] .gitignore configurado (não enviar venv, .env, logs)

### 2. Arquivos Essenciais
- [x] `requirements.txt` - Dependências Python
- [x] `Procfile` - Comando de inicialização (Heroku)
- [x] `render.yaml` - Config Render
- [x] `Dockerfile` - Container Docker
- [x] `.dockerignore` - Ignorar arquivos no Docker

### 3. Configuração Backend
- [ ] CORS configurado com domínio do frontend
- [ ] Variáveis de ambiente prontas
- [ ] Modelo treinado existe em `src/model/saved_models/`
- [ ] Health check funcionando (`/health`)

### 4. Configuração Frontend
- [x] API_URL detecta automaticamente produção/dev
- [ ] Testar localmente antes do deploy

### 5. Testes Locais
```bash
# Testar backend
uvicorn src.backend.main:app --reload

# Acessar http://localhost:8000/docs
# Verificar se /health retorna 200 OK
```

### 6. Modelos e Dados
- [ ] `src/model/saved_models/regression_model.pkl` existe
- [ ] Scalers existem no diretório
- [ ] Tamanho total < 500MB (limite grátis)

### 7. Documentação
- [x] README.md atualizado
- [x] DEPLOY_GUIDE.md disponível
- [x] API documentada com FastAPI

## Comandos Úteis

### Git
```bash
git status
git add .
git commit -m "Deploy ready"
git push origin main
```

### Testar localmente
```bash
# Backend
.\venv\Scripts\Activate.ps1
uvicorn src.backend.main:app --reload

# Frontend (outro terminal)
python -m http.server 3000 --directory src/frontend
```

### Docker (opcional)
```bash
docker build -t energyflow .
docker run -p 8000:8000 energyflow
```

## Deploy Rápido

Escolha uma opção:

1. **Render** - Mais fácil e completo
2. **Railway** - Mais rápido
3. **Heroku** - Mais conhecido
4. **VPS** - Mais controle

Veja detalhes em: [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
