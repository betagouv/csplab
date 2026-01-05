#!/usr/bin/env bash

# We may expect that the following environment variables are set:
#
#   - PORT: the server port
#   - TYCHO_DEBUG: activate the debug mode (for development) [*]
#
# [*] optional

set -euo pipefail

declare -i debug=${TYCHO_DEBUG:-0}


if [ ${debug} == 1 ]; then
  echo "⚗️ DEBUG mode activated. We hope your are not running in production. 🤞"
  echo "🚀 Starting development server"
  python3 manage.py runserver "0.0.0.0:${PORT}"
else
  echo "PRODUCTION mode activated."
  echo "🚀 Starting server"
  gunicorn config.wsgi:application --log-file -
fi
