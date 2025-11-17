Render Deploy — Modelo treinado

Resumo rápido:
- O backend espera encontrar o modelo em `src/model/saved_models/regression_model.pkl` (ou toda a pasta `src/model/saved_models/`).
- Evite commitar binários grandes no Git. Use um storage externo (S3, GCS, Azure Blob) e passe uma URL para o Render.

Opções suportadas neste repositório:

1) Runtime download (startup)
   - Defina a variável de ambiente MODEL_URL no painel do Render apontando para o arquivo .pkl ou um .zip que contenha src/model/saved_models/.
   - Ao iniciar, o backend tentará baixar a URL. Se for .zip, será extraído no diretório do projeto.
   - Vantagem: imagem pequena, trocar modelo sem rebuild.

2) Build-time download (durante build)
   - Forneça MODEL_URL durante o build (Render build env) — o render.yaml e Dockerfile já possuem lógica para baixar/extrair durante o build.
   - Vantagem: modelo já presente na imagem; útil quando não se quer download em runtime.

3) Incluir modelo no repositório (não recomendado)
   - Coloque src/model/saved_models/regression_model.pkl no repositório antes do build. O Dockerfile copia src/ para a imagem.
   - Desvantagem: aumenta histórico e tamanho do repositório.

Como usar a opção 1 (recomendado):

- No painel do Render, vá em Environment do serviço energyflow-api e crie uma variável:
  - MODEL_URL = https://.../regression_model.zip (ou .pkl)
- Reinicie o serviço.
- Cheque logs: procure por mensagens relacionadas ao download/extract do modelo.

Comandos locais de verificação:

PowerShell:
Invoke-RestMethod -Uri 'http://localhost:8000/health'
Invoke-RestMethod -Uri 'http://localhost:8000/model/info'

Shell (Linux/macOS):
export MODEL_URL=https://.../regression_model.zip
./scripts/download_model.sh
python -m src.backend.main
curl http://localhost:8000/health

Se precisar, eu posso:
- Gerar o artefato .zip com a pasta src/model/saved_models/ pronta.
- Ajudar a fazer upload para S3 e gerar uma URL pré-assinada.
