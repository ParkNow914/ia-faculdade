#!/usr/bin/env bash
# Download and extract model artifact for local testing or CI
set -euo pipefail

if [ -z "${MODEL_URL:-}" ]; then
  echo "USO: MODEL_URL environment variable must be set"
  echo "Example: MODEL_URL=https://.../regression_model.zip ./scripts/download_model.sh"
  exit 1
fi

mkdir -p src/model/saved_models
TMPFILE="/tmp/$(basename "$MODEL_URL")"
echo "🔁 Baixando $MODEL_URL -> $TMPFILE"
curl -fSL "$MODEL_URL" -o "$TMPFILE"

if file "$TMPFILE" | grep -qi zip; then
  echo "📦 Extraindo zip..."
  unzip -o "$TMPFILE" -d .
  rm -f "$TMPFILE"
else
  echo "📁 Movendo artefato para src/model/saved_models/regression_model.pkl"
  mv "$TMPFILE" src/model/saved_models/regression_model.pkl || (echo "Falha ao mover" && exit 1)
fi

echo "✅ Modelo instalado em src/model/saved_models/"
