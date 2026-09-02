"""Print `export NAME=value` lines for every secret under /{service}/{SCALEWAY_ENV}.

Meant to be eval'd by a shell script before a service's process starts (see
each service's bin/inject_scaleway_env.sh), so config lives in Scaleway
Secret Manager instead of being set by hand (dev, and prod's Scalingo
dashboard alike). Scaleway API credentials (SCW_ACCESS_KEY, SCW_SECRET_KEY,
SCW_DEFAULT_PROJECT_ID, SCW_DEFAULT_REGION) are still real env vars, read the
same way the `scw` CLI reads them.
"""

from __future__ import annotations

import base64
import os
import shlex
import sys

from scaleway import Client
from scaleway.secret.v1beta1 import SecretV1Beta1API


def main(service: str) -> None:
    env = os.environ.get("SCALEWAY_ENV")
    if not env:
        return
    secret_path = f"/{service}/{env}"

    client = Client.from_env()
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
