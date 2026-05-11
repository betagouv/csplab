#!/usr/bin/env bash
set -euo pipefail

# Start the webserver
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
