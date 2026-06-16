#!/usr/bin/env bash
set -euo pipefail

# Start Flower in the background so the web process can proxy to it via localhost
if [ -n "${FLOWER_PORT:-}" ] && [ -n "${FLOWER_BASIC_AUTH_USER:-}" ] && [ -n "${FLOWER_BASIC_AUTH_PASSWORD:-}" ]; then
    celery -A infrastructure.celery_app flower \
        --port="$FLOWER_PORT" \
        --url-prefix=flower \
        --basic-auth="$FLOWER_BASIC_AUTH_USER:$FLOWER_BASIC_AUTH_PASSWORD" &
fi

exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
