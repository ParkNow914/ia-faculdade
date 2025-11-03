# 🚀 Guia Completo de Deploy - EnergyFlow AI

## 📋 Índice
1. [Opção 1: Render (Gratuito e Fácil)](#opção-1-render-recomendado)
2. [Opção 2: Railway (Gratuito)](#opção-2-railway)
3. [Opção 3: Heroku](#opção-3-heroku)
4. [Opção 4: DigitalOcean/AWS/Azure (Produção)](#opção-4-vps-digitalocean-aws-azure)
5. [Opção 5: Vercel + Render](#opção-5-vercel--render-híbrido)

---

## 🎯 Opção 1: Render (RECOMENDADO)

### ✅ Vantagens
- ✅ Gratuito (750h/mês)
- ✅ Deploy automático do GitHub
- ✅ HTTPS grátis
- ✅ Fácil configuração
- ✅ Suporta Python e sites estáticos

### 📝 Passo a Passo

#### 1. Preparar Repositório GitHub
```bash
# No seu terminal
git add .
git commit -m "Preparar para deploy"
git push origin main
```

#### 2. Deploy do Backend (API)
1. Acesse [render.com](https://render.com)
2. Crie conta (use GitHub)
3. Clique em **"New +"** → **"Web Service"**
4. Conecte seu repositório `ia-faculdade`
5. Configure:
   - **Name**: `energyflow-api`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: deixe vazio
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

6. **Variáveis de Ambiente** (Environment):
   ```
   PYTHON_VERSION=3.10.0
   DEBUG=False
   LOG_LEVEL=INFO
   ```

7. Clique em **"Create Web Service"**
8. Aguarde o deploy (5-10 min)
9. Sua API estará em: `https://energyflow-api.onrender.com`

#### 3. Deploy do Frontend (Site Estático)
1. No Render, clique em **"New +"** → **"Static Site"**
2. Conecte o mesmo repositório
3. Configure:
   - **Name**: `energyflow-frontend`
   - **Branch**: `main`
   - **Root Directory**: deixe vazio
   - **Build Command**: `echo "No build needed"`
   - **Publish Directory**: `src/frontend`

4. **Variáveis de Ambiente**:
   ```
   API_URL=https://energyflow-api.onrender.com
   ```

5. Clique em **"Create Static Site"**
6. Aguarde o deploy
7. Seu site estará em: `https://energyflow-frontend.onrender.com`

#### 4. Atualizar Frontend para Usar API do Render
No arquivo `src/frontend/js/app.js`, atualize:
```javascript
const API_URL = 'https://energyflow-api.onrender.com';
```

---

## 🎯 Opção 2: Railway

### ✅ Vantagens
- Gratuito (500h/mês + $5 crédito)
- Deploy automático
- Super fácil

### 📝 Passo a Passo

1. Acesse [railway.app](https://railway.app)
2. Login com GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. Selecione `ia-faculdade`
5. Railway detecta automaticamente Python
6. Adicione variáveis de ambiente:
   ```
   PORT=8000
   DEBUG=False
   ```
7. Deploy automático!
8. Clique em **"Generate Domain"** para ter URL pública

---

## 🎯 Opção 3: Heroku

### 📝 Criar arquivo Procfile
```bash
web: uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT
```

### 📝 Passo a Passo
1. Crie conta no [Heroku](https://heroku.com)
2. Instale Heroku CLI:
   ```bash
   # Windows (PowerShell como Admin)
   winget install Heroku.HerokuCLI
   ```

3. Deploy:
   ```bash
   heroku login
   heroku create energyflow-ai
   git push heroku main
   heroku open
   ```

---

## 🎯 Opção 4: VPS (DigitalOcean/AWS/Azure)

### 💰 Custo: ~$5-10/mês

### 📝 Passo a Passo (DigitalOcean)

#### 1. Criar Droplet
- Ubuntu 22.04
- $6/mês (1GB RAM)
- Escolha região próxima

#### 2. Conectar via SSH
```bash
ssh root@SEU_IP
```

#### 3. Instalar Dependências
```bash
# Atualizar sistema
apt update && apt upgrade -y

# Instalar Python, pip, nginx
apt install -y python3.10 python3-pip nginx git

# Instalar Docker (opcional)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### 4. Clonar Projeto
```bash
cd /var/www
git clone https://github.com/SEU_USUARIO/ia-faculdade.git
cd ia-faculdade
```

#### 5. Instalar Dependências Python
```bash
pip3 install -r requirements.txt
```

#### 6. Configurar Nginx
```bash
nano /etc/nginx/sites-available/energyflow
```

Cole:
```nginx
server {
    listen 80;
    server_name SEU_DOMINIO.com;

    # Frontend
    location / {
        root /var/www/ia-faculdade/src/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Ativar:
```bash
ln -s /etc/nginx/sites-available/energyflow /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 7. Criar Serviço Systemd
```bash
nano /etc/systemd/system/energyflow.service
```

Cole:
```ini
[Unit]
Description=EnergyFlow AI Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/ia-faculdade
Environment="PATH=/usr/bin"
ExecStart=/usr/local/bin/uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Ativar:
```bash
systemctl daemon-reload
systemctl start energyflow
systemctl enable energyflow
systemctl status energyflow
```

#### 8. SSL (HTTPS) Grátis
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d SEU_DOMINIO.com
```

---

## 🎯 Opção 5: Vercel + Render (HÍBRIDO)

### Frontend no Vercel (Grátis)
1. Acesse [vercel.com](https://vercel.com)
2. Import repository
3. Configure:
   - **Framework Preset**: `Other`
   - **Root Directory**: `src/frontend`
   - **Build Command**: deixe vazio
   - **Output Directory**: `.`

### Backend no Render (Grátis)
Siga os passos da Opção 1 para o backend

---

## 🔧 Configurações Importantes

### 1. Atualizar CORS no Backend
Edite `src/backend/core/config.py`:
```python
CORS_ORIGINS: list = [
    "https://energyflow-frontend.onrender.com",
    "https://seu-dominio.vercel.app",
    "http://localhost:3000",  # desenvolvimento
]
```

### 2. Atualizar API_URL no Frontend
Edite `src/frontend/js/app.js`:
```javascript
// Detectar automaticamente
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : 'https://energyflow-api.onrender.com';
```

### 3. Criar arquivo .env (não commitar!)
```bash
DEBUG=False
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

---

## 📊 Comparação de Opções

| Plataforma | Custo | Facilidade | Performance | HTTPS |
|------------|-------|------------|-------------|-------|
| **Render** | ⭐ Grátis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ Auto |
| **Railway** | ⭐ Grátis | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Auto |
| **Heroku** | ⭐⭐ $7/mês | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Auto |
| **VPS** | ⭐⭐ $5-10/mês | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⚙️ Manual |
| **Vercel+Render** | ⭐ Grátis | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Auto |

---

## ⚡ Quick Start (Render - Mais Rápido)

1. **Push para GitHub**
   ```bash
   git add .
   git commit -m "Deploy ready"
   git push
   ```

2. **Render Backend**
   - Vá em render.com → New Web Service
   - Conecte repo → Python
   - Start: `uvicorn src.backend.main:app --host 0.0.0.0 --port $PORT`
   - Deploy!

3. **Render Frontend**
   - New Static Site
   - Publish dir: `src/frontend`
   - Deploy!

4. **Atualizar API_URL** no frontend com URL do backend

5. **Done! 🎉**

---

## 🐛 Troubleshooting

### Erro: "Module not found"
- Certifique-se que `requirements.txt` está completo
- Verifique Python version (3.10)

### Erro: "Port already in use"
- Use `$PORT` em vez de porta fixa no comando

### Erro CORS
- Adicione domínio do frontend em `CORS_ORIGINS`

### Site não carrega
- Verifique se backend está rodando: `https://seu-api.onrender.com/health`
- Verifique console do navegador (F12)

---

## 📞 Suporte

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- FastAPI Deploy: https://fastapi.tiangolo.com/deployment/

---

**🎯 RECOMENDAÇÃO FINAL**: Use **Render** para começar (100% grátis, fácil, HTTPS automático).
Quando precisar escalar, migre para VPS ou AWS.
