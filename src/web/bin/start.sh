#!/usr/bin/env bash

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/inject_scaleway_env.sh"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.base}"

echo "PRODUCTION mode activated."
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🚀 Starting server"
gunicorn config.wsgi:application --log-file -
