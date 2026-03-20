#!/usr/bin/env bash
set -euo pipefail

# Configuration Tesseract pour Scalingo
export TESSDATA_PREFIX="/app/.apt/usr/share/tesseract-ocr/4.00/tessdata"
TESSDATA_DIR="$TESSDATA_PREFIX"

mkdir -p "$TESSDATA_DIR"

# Télécharge fra.traineddata si absent
if [ ! -f "$TESSDATA_DIR/fra.traineddata" ]; then
  echo "[boot] Installing fra.traineddata into $TESSDATA_DIR"
  curl -fL --retry 3 -o "$TESSDATA_DIR/fra.traineddata" \
    https://github.com/tesseract-ocr/tessdata_fast/raw/main/fra.traineddata
  chmod 0644 "$TESSDATA_DIR/fra.traineddata"
fi

# Lancer le serveur web OCR
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
