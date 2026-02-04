#!/usr/bin/env bash

set -euo pipefail

echo "PRODUCTION mode activated."
echo "🚀 Starting server"
gunicorn config.wsgi:application --log-file -
