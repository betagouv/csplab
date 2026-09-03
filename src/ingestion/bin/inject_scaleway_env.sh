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
        return 1
    fi
    lib_dir="$(dirname "${BASH_SOURCE[0]}")/../../../libs/scaleway_secrets"
    if command -v uv >/dev/null 2>&1; then
        fetch=(uv run -q --project "$lib_dir" python -m scaleway_secrets.fetch ingestion)
    else
        fetch=(python -m scaleway_secrets.fetch ingestion)
    fi
    if [ "$SCALEWAY_ENV" = "prod" ]; then
        scaleway_env="$("${fetch[@]}")" || return 1
    else
        scaleway_env="$("${fetch[@]}" 2>/dev/null)" || return 1
    fi
    eval "$scaleway_env"
fi
