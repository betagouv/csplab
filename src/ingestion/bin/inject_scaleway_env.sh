#!/usr/bin/env bash
# Meant to be sourced (not executed) so the exported vars persist in the
# caller's shell, e.g.: `source "$(dirname "$0")/inject_scaleway_env.sh"`
#
# No-op unless SCALEWAY_SECRET_PATH is set (e.g. /ingestion/prod), so it is
# safe to source everywhere: locally, in CI, and in every Procfile process.
if [ -n "${SCALEWAY_SECRET_PATH:-}" ]; then
    scaleway_env="$(python "$(dirname "${BASH_SOURCE[0]}")/fetch_scaleway_secrets.py")"
    eval "$scaleway_env"
fi
