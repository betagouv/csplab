#!/usr/bin/env bash
set -euo pipefail

exec celery -A infrastructure.celery_app flower --port=$PORT --basic-auth=$FLOWER_BASIC_AUTH_USER:$FLOWER_BASIC_AUTH_PASSWORD
