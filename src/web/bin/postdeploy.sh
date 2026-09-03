#!/usr/bin/env bash

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/inject_scaleway_env.sh"

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.base}"

echo "🗃️ Apply new migrations"
python3 manage.py migrate --noinput
