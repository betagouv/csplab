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
from collections.abc import Iterable
from pathlib import Path

from scaleway import Client
from scaleway.secret.v1beta1 import Secret, SecretV1Beta1API
from scaleway_core.profile import Profile


def _secret_manager() -> tuple[SecretV1Beta1API, str | None]:
    config_file = Path(Profile.get_default_config_file_path())
    client = (
        Client.from_config_file_and_env() if config_file.exists() else Client.from_env()
    )
    # The Scaleway SDK auto-fills organization_id from the profile on every
    # request; combined with project_id, the API silently returns zero
    # secrets instead of an error. Clear it so listing stays project-scoped.
    # https://github.com/scaleway/scaleway-sdk-python/issues/2147
    client.default_organization_id = None
    return SecretV1Beta1API(client), client.default_project_id


def _list_secrets(
    api: SecretV1Beta1API, project_id: str | None, service: str, env: str
) -> list[Secret]:
    return api.list_secrets_all(
        path=f"/{service}/{env}",
        scheduled_for_deletion=False,
        project_id=project_id,
    )


def _access_value(api: SecretV1Beta1API, secret: Secret) -> str:
    response = api.access_secret_version(secret_id=secret.id, revision="latest_enabled")
    return base64.b64decode(response.data).decode("utf-8")


def fetch_secrets(services: Iterable[str], env: str) -> list[tuple[str, str, str]]:
    """Return (service, NAME, value) for every secret under /{service}/{env}.

    Unlike main(), env vars already set in the process never hide a secret.
    """
    api, project_id = _secret_manager()
    return [
        (service, secret.name.upper(), _access_value(api, secret))
        for service in services
        for secret in _list_secrets(api, project_id, service, env)
    ]


def main(service: str, names_only: bool = False) -> None:
    env = os.environ.get("SCALEWAY_ENV")
    if not env:
        return
    api, project_id = _secret_manager()

    for secret in _list_secrets(api, project_id, service, env):
        name = secret.name.upper()
        if names_only:
            print(name)
            continue
        if os.environ.get(name):
            continue  # a real Scalingo env var was set by hand: it wins
        print(f"export {name}={shlex.quote(_access_value(api, secret))}")


def cli() -> None:
    args = [arg for arg in sys.argv[1:] if arg != "--names"]
    if len(args) != 1:
        usage = "usage: python -m scaleway_secrets.fetch <service> [--names]"
        print(usage, file=sys.stderr)
        raise SystemExit(1)
    main(args[0], names_only="--names" in sys.argv)


if __name__ == "__main__":
    cli()
