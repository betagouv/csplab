#!/usr/bin/env bash

set -euo pipefail

# ---------------------------------------------------------------------------
# backup-db-to-scaleway.sh — Fetch the latest Scalingo backup of the
# csplab-web PostgreSQL database and archive it to Scaleway Object Storage.
#
# Required env vars (fetched from Scaleway Secret Manager under
# /web/{SCALEWAY_ENV} when SCALEWAY_ENV is set):
#   DB_BACKUP_SCALINGO_API_TOKEN            Scalingo API token
#   DB_BACKUP_SCALINGO_POSTGRESQL_ADDON_ID  UUID of the PostgreSQL addon (scalingo --app csplab-web addons)
#   DB_BACKUP_SCW_ACCESS_KEY_ID             Scaleway access key
#   DB_BACKUP_SCW_SECRET_ACCESS_KEY         Scaleway secret key
#   DB_BACKUP_SCW_BUCKET                    Target bucket name
#
# Optional env vars:
#   DB_BACKUP_SCALINGO_APP   Scalingo app name (default: csplab-web)
#   DB_BACKUP_SCW_REGION     Scaleway region (default: fr-par)
#   DB_BACKUP_SCW_ENDPOINT   Scaleway S3 endpoint (default: https://s3.${DB_BACKUP_SCW_REGION}.scw.cloud)
#
# Requires the `scalingo` and `aws` CLIs to be installed and authenticated.
# ---------------------------------------------------------------------------

# No-op unless SCALEWAY_ENV is set (same pattern as bin/inject_scaleway_env.sh):
# pulls every secret under /web/{SCALEWAY_ENV} and exports it, so these
# DB_BACKUP_-scoped credentials live in Secret Manager alongside the rest of
# the web app's config instead of being set by hand.
if [ -n "${SCALEWAY_ENV:-}" ]; then
  if [ "$SCALEWAY_ENV" = "prod" ] && [ -z "${SCALINGO_APPLICATION_ID:-}" ]; then
    echo "SCALEWAY_ENV=prod is only allowed on Scalingo (SCALINGO_APPLICATION_ID not set)" >&2
    exit 1
  fi
  scaleway_env="$(python -m scaleway_secrets.fetch web)"
  eval "$scaleway_env"
fi

SCALINGO_APP="${DB_BACKUP_SCALINGO_APP:-csplab-web}"
SCW_REGION="${DB_BACKUP_SCW_REGION:-fr-par}"
SCW_ENDPOINT="${DB_BACKUP_SCW_ENDPOINT:-https://s3.${SCW_REGION}.scw.cloud}"

install_scalingo_cli() {
  echo "📥 Installing Scalingo CLI…"
  if [[ "$(uname -s)" == "Darwin" ]] && command -v brew &>/dev/null; then
    brew install scalingo
  else
    curl -fsSO https://cli-dl.scalingo.com/install
    bash install -i $HOME/bin
  fi
}

install_aws_cli() {
  echo "📥 Installing AWS CLI…"
  if [[ "$(uname -s)" == "Darwin" ]] && command -v brew &>/dev/null; then
    brew install awscli
  else
    local zip="$HOME/awscliv2.zip"
    curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "$zip"
    unzip -q "$zip" -d "$HOME"
    "$HOME/aws/install" -i "$HOME/aws-cli" -b "$HOME/bin"
  fi
}

for var in DB_BACKUP_SCALINGO_API_TOKEN DB_BACKUP_SCALINGO_POSTGRESQL_ADDON_ID DB_BACKUP_SCW_ACCESS_KEY_ID DB_BACKUP_SCW_SECRET_ACCESS_KEY DB_BACKUP_SCW_BUCKET; do
  if [[ -z "${!var:-}" ]]; then
    echo "❌ Missing required env var: $var"
    exit 1
  fi
done

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

mkdir -p "$HOME/bin"
export PATH="$PATH:$HOME/bin"

command -v scalingo &>/dev/null || install_scalingo_cli
command -v aws &>/dev/null || install_aws_cli


scalingo login --api-token "$DB_BACKUP_SCALINGO_API_TOKEN"

echo "📦 Fetching latest backup for ${SCALINGO_APP} (addon ${DB_BACKUP_SCALINGO_POSTGRESQL_ADDON_ID})…"
scalingo --app "$SCALINGO_APP" --addon "$DB_BACKUP_SCALINGO_POSTGRESQL_ADDON_ID" \
  backups-download --output "$WORKDIR" --silent

BACKUP=$(ls -t "$WORKDIR"/* 2>/dev/null | head -1)
if [[ -z "$BACKUP" ]]; then
  echo "❌ No backup file was downloaded."
  exit 1
fi

DEST="s3://${DB_BACKUP_SCW_BUCKET}/csplab-web/$(date +%Y/%m)/$(basename "$BACKUP")"

echo "🚀 Uploading $(basename "$BACKUP") to ${DEST}…"
AWS_ACCESS_KEY_ID="$DB_BACKUP_SCW_ACCESS_KEY_ID" \
AWS_SECRET_ACCESS_KEY="$DB_BACKUP_SCW_SECRET_ACCESS_KEY" \
  aws s3 cp "$BACKUP" "$DEST" \
    --endpoint-url "$SCW_ENDPOINT" \
    --region "$SCW_REGION"

echo "✅ Done. Backup archived at ${DEST}."
