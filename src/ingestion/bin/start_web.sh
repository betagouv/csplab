#!/usr/bin/env bash
set -euo pipefail

# Start Flower in the background so the web process can proxy to it via localhost.
# Scalingo only supervises uvicorn, so restart Flower ourselves if it exits
# (e.g. killed by the OOM killer).
if [ -n "${FLOWER_PORT:-}" ] && [ -n "${FLOWER_BASIC_AUTH_USER:-}" ] && [ -n "${FLOWER_BASIC_AUTH_PASSWORD:-}" ]; then
    (
        while true; do
            celery -A infrastructure.celery_app flower \
                --port="$FLOWER_PORT" \
                --url-prefix=flower \
                --basic-auth="$FLOWER_BASIC_AUTH_USER:$FLOWER_BASIC_AUTH_PASSWORD" \
                && status=0 || status=$?
            echo "Flower exited with status $status, restarting in 5s" >&2
            sleep 5
        done
    ) &
fi

exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
