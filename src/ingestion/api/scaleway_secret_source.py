from __future__ import annotations

import base64
import os
from http import HTTPStatus
from typing import Mapping

from pydantic_settings import BaseSettings
from pydantic_settings.sources import EnvSettingsSource
from scaleway import Client
from scaleway.secret.v1beta1 import SecretV1Beta1API
from scaleway_core.api import ScalewayException

_FORBIDDEN_ENVS = {"prod", "production"}


class ScalewaySecretSettingsSource(EnvSettingsSource):
    """Loads settings from Scaleway Secret Manager, one secret per env value.

    Each field is looked up as its own secret, named after the field (e.g.
    "database_url") under the "/ingestion/{SCALEWAY_ENV}" directory (e.g.
    "/ingestion/dev"). Fields with no matching secret are silently skipped,
    falling through to the next settings source. Scaleway API credentials
    (SCW_ACCESS_KEY, SCW_SECRET_KEY, SCW_DEFAULT_PROJECT_ID,
    SCW_DEFAULT_REGION) are read from the environment the same way the `scw`
    CLI does, so a developer already authenticated with `scw` needs nothing
    extra locally.

    This source is for dev/CI use only: production gets its config from real
    env vars (Scalingo), which always take priority, so SCALEWAY_ENV must
    never be set to prod/production.
    """

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        env = os.getenv("SCALEWAY_ENV")
        if env is not None and env.lower() in _FORBIDDEN_ENVS:
            raise ValueError(
                f"SCALEWAY_ENV={env!r} is not allowed: this source is for "
                "dev/CI use only, production must use real env vars."
            )
        self._secret_path = f"/ingestion/{env}" if env else None
        super().__init__(settings_cls)

    def _load_env_vars(self) -> Mapping[str, str | None]:
        if not self._secret_path:
            return {}

        client = Client.from_env()
        api = SecretV1Beta1API(client)

        env_vars: dict[str, str | None] = {}
        for field_name in self.settings_cls.model_fields:
            try:
                response = api.access_secret_version_by_path(
                    secret_path=self._secret_path,
                    secret_name=field_name,
                    revision="latest_enabled",
                )
            except ScalewayException as exc:
                if exc.status_code == HTTPStatus.NOT_FOUND:
                    continue
                raise
            env_vars[field_name] = base64.b64decode(response.data).decode("utf-8")

        return env_vars
