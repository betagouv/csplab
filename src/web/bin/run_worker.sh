#!/usr/bin/env bash

set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.base}"

# CONTAINER is set by Scalingo with format "worker-1", "worker-2", etc.
INDEX="${CONTAINER##*-}"

if [ "$INDEX" = "1" ]; then
    echo "Instance 1: starting Huey with scheduler and workers"
    python manage.py run_huey
else
    echo "Instance ${INDEX}: starting Huey workers only (no scheduler)"
    python manage.py run_huey --no-periodic
fi
