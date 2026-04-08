#!/usr/bin/env bash

set -euo pipefail

echo "PRODUCTION mode activated."
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🚀 Starting server"
gunicorn config.wsgi:application -w 5 --log-file -
