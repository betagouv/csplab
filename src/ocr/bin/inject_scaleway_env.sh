#!/usr/bin/env bash
# Meant to be sourced (not executed) so the exported vars persist in the
# caller's shell, e.g.: `source "$(dirname "$0")/inject_scaleway_env.sh"`
#
# This is the only way the app gets its config: dev, CI, and prod (Scalingo)
# all set SCALEWAY_ENV (e.g. dev, prod) and source this before the app
# starts. No-op unless SCALEWAY_ENV is set, so it is safe to source
# everywhere, including plain CI runs that set real env vars by hand instead.
if [ -n "${SCALEWAY_ENV:-}" ]; then
    if [ "$SCALEWAY_ENV" = "prod" ] && [ -z "${SCALINGO_APPLICATION_ID:-}" ]; then
        echo "SCALEWAY_ENV=prod is only allowed on Scalingo (SCALINGO_APPLICATION_ID not set)" >&2
        exit 1
    fi
    scaleway_env="$(python -m scaleway_secrets.fetch ocr)"
    eval "$scaleway_env"
fi
