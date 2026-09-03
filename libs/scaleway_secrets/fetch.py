"""Print `export NAME=value` lines for every secret under /{service}/{SCALEWAY_ENV}.

Meant to be eval'd by a shell script before a service's process starts (see
each service's bin/inject_scaleway_env.sh), so config lives in Scaleway
Secret Manager instead of being set by hand (dev, and prod's Scalingo
dashboard alike). Scaleway API credentials come from the `scw` CLI config
file (`scw init`) or from the SCW_ACCESS_KEY, SCW_SECRET_KEY,
SCW_DEFAULT_PROJECT_ID and SCW_DEFAULT_REGION env vars, which take precedence.
"""

from __future__ import annotations

import base64
import os
import shlex
import sys
from pathlib import Path

from scaleway import Client
from scaleway.secret.v1beta1 import SecretV1Beta1API
from scaleway_core.profile import Profile


def main(service: str) -> None:
    env = os.environ.get("SCALEWAY_ENV")
    if not env:
        return
    secret_path = f"/{service}/{env}"

    config_file = Path(Profile.get_default_config_file_path())
    client = (
        Client.from_config_file_and_env() if config_file.exists() else Client.from_env()
    )
    api = SecretV1Beta1API(client)

    for secret in api.list_secrets_all(path=secret_path, scheduled_for_deletion=False):
        name = secret.name.upper()
        if os.environ.get(name):
            continue  # a real Scalingo env var was set by hand: it wins
        response = api.access_secret_version(
            secret_id=secret.id, revision="latest_enabled"
        )
        value = base64.b64decode(response.data).decode("utf-8")
        print(f"export {name}={shlex.quote(value)}")


def cli() -> None:
    if len(sys.argv) != 2:
        print("usage: python -m scaleway_secrets.fetch <service>", file=sys.stderr)
        raise SystemExit(1)
    main(sys.argv[1])


if __name__ == "__main__":
    cli()
