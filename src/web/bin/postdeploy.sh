#!/usr/bin/env bash

set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.base}"

echo "🗃️ Apply new migrations"
python3 manage.py migrate --noinput
