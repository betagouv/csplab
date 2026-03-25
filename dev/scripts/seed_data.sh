#!/usr/bin/env bash
set -euo pipefail

echo "loading env vars"
set -a                 # auto-export variables
source ./env.d/postgresql
source ./env.d/ocr
set +a

COLLECTION="fonction_publique"
SNAPSHOT_PATH="./dev/datas/qdrant_fonction_publique.snapshot"
SQL_PATH="./dev/datas/offers.sql"

echo "loading qdrant snapshot"
curl -X POST "http://localhost:6333/collections/${COLLECTION}/snapshots/upload?priority=snapshot" \
  -H "Content-Type:multipart/form-data" \
  -H "api-key: ${API_KEY}" \
  -F "snapshot=@${SNAPSHOT_PATH}"

echo "loading offers in db"
PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" < "$SQL_PATH"
