"""Configuration for ingestion app."""

import environ
from pydantic import BaseModel, HttpUrl

env = environ.Env()


class PisteConfig(BaseModel):
    """Configuration for PISTE API client."""

    oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    client_id: str
    client_secret: str


class IngestionConfig(BaseModel):
    """Configuration for ingestion app."""

    piste: PisteConfig

    def __init__(self, piste_config: PisteConfig):
        """Create configuration from PISTE config."""
        super().__init__(piste=piste_config)
