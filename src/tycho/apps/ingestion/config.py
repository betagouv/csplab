"""Configuration for ingestion app."""

import environ
from pydantic import BaseModel, HttpUrl

# Use django-environ for reading environment variables
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

    def __init__(self, piste_env: PisteConfig):
        """Create configuration from environment variables."""
        super().__init__(piste=piste_env)
