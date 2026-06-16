#!/usr/bin/env bash
set -euo pipefail

exec celery -A infrastructure.celery_app worker --loglevel=info
