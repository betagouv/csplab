#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/inject_scaleway_env.sh"

exec celery -A infrastructure.celery_app worker --loglevel=info
