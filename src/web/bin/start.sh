#!/usr/bin/env bash

set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.base}"

echo "PRODUCTION mode activated."
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Same default as gunicorn without --bind, which it drops once one is given.
if [[ -n "${PORT:-}" ]]; then
    binds=(--bind "0.0.0.0:${PORT}")
else
    binds=(--bind "127.0.0.1:8000")
fi
# Scalingo private network only: a fixed port, as $PORT is not guaranteed
# to be stable and is not advertised to the other apps of the network.
# Skipped when $PORT is 8000: 0.0.0.0 already covers the private interface.
# https://doc.scalingo.com/platform/networking/private/working-with-private-networks
if [[ -n "${SCALINGO_PRIVATE_HOSTNAME:-}" && "${PORT:-}" != "8000" ]]; then
    binds+=(--bind "${SCALINGO_PRIVATE_HOSTNAME}:8000")
fi

echo "🚀 Starting server"
gunicorn config.wsgi:application "${binds[@]}" --log-file -
