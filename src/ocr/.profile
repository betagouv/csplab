# Sourced by Scalingo at container start (web, worker, one-off `scalingo run`).
if [ -z "${SCALEWAY_ENV_INJECTED:-}" ]; then
    source "$HOME/bin/inject_scaleway_env.sh" && export SCALEWAY_ENV_INJECTED=1
fi
