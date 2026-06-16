#!/usr/bin/env bash
set -euo pipefail

exec celery -A infrastructure.celery_app flower --port=$FLOWER_PORT --url-prefix=flower --basic-auth=$FLOWER_BASIC_AUTH_USER:$FLOWER_BASIC_AUTH_PASSWORD
