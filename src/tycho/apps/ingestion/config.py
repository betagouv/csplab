"""Configuration for ingestion app."""

from typing import cast

import environ
from pydantic import BaseModel, HttpUrl


class PisteConfig(BaseModel):
    """Configuration for PISTE API client."""

    oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    client_id: str
    client_secret: str


class IngestionConfig(BaseModel):
    """Configuration for ingestion app."""

    piste: PisteConfig

    @classmethod
    def from_environment(cls) -> "IngestionConfig":
        """Create configuration from environment variables.

        Returns:
            IngestionConfig instance with values from environment
        """
        env = environ.Env()
        return cls(
            piste=PisteConfig(
                oauth_base_url=HttpUrl(cast(str, env("TYCHO_PISTE_OAUTH_BASE_URL"))),
                ingres_base_url=HttpUrl(cast(str, env("TYCHO_INGRES_BASE_URL"))),
                client_id=cast(str, env("TYCHO_INGRES_CLIENT_ID")),
                client_secret=cast(str, env("TYCHO_INGRES_CLIENT_SECRET")),
            )
        )
