#
# Bash library for utility scripts
#
# shellcheck shell=bash

declare DOCKER_USER
declare -i DOCKER_UID
declare -i DOCKER_GID

DOCKER_UID="$(id -u)"
DOCKER_GID="$(id -g)"
# Use a higher GID for MacOS users to prevent permission issues with the default
# GID=20
if [[ "${OSTYPE}" =~ "darwin" ]]; then
  DOCKER_GID=1000
fi
DOCKER_USER="${DOCKER_UID}:${DOCKER_GID}"

export DOCKER_UID
export DOCKER_GID
export DOCKER_USER


function compose(){

  docker compose "$@"
}


function compose_run(){

  if [[ -z "${2}" ]]; then
    echo "usage: compose_run [--no-deps] SERVICE COMMAND"
    exit 1
  fi

  # Arguments
  declare -i no_deps
  if [[ "$1" == "--no-deps" ]]; then
    no_deps=1
    shift
  fi

  declare service="${1}"
  shift

  declare user="${DOCKER_USER}"
  declare volume="./src/${service}:/app"
  declare -a args=(--rm --user "${user}" --volume "${volume}")

  # Prevent 'the input device is not a TTY' error from `docker compose run`
  # by disabling TTY when standard output is not a TTY
  if [[ "$(tty 2>/dev/null)" == "not a tty" ]]; then
    args+=(--no-TTY)
  fi

  # Do not run related services
  if [[ no_deps -eq 1 ]]; then
    args+=(--no-deps)
  fi

  compose run \
    "${args[@]}" \
    "${service}" \
    "$@"
}
