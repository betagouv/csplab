#!/usr/bin/env python
"""Print `export NAME=value` lines for every secret under SCALEWAY_SECRET_PATH.

Meant to be eval'd by a shell script before the app process starts (see
inject_scaleway_env.sh), so production config lives in Scaleway Secret
Manager instead of being set by hand in Scalingo's dashboard. Scaleway API
credentials (SCW_ACCESS_KEY, SCW_SECRET_KEY, SCW_DEFAULT_PROJECT_ID,
SCW_DEFAULT_REGION) are still real Scalingo env vars, read the same way the
`scw` CLI reads them.
"""

from __future__ import annotations

import base64
import os
import shlex

from scaleway import Client
from scaleway.secret.v1beta1 import SecretV1Beta1API


def main() -> None:
    secret_path = os.environ.get("SCALEWAY_SECRET_PATH")
    if not secret_path:
        return

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


if __name__ == "__main__":
    main()
