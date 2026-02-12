"""Configuration for ingestion app."""

from pydantic import BaseModel, HttpUrl


class PisteConfig(BaseModel):
    """Configuration for PISTE API client."""

    oauth_base_url: HttpUrl
    ingres_base_url: HttpUrl
    client_id: str
    client_secret: str


class PisteGatewayConfig(BaseModel):
    """Configuration for ingestion app."""

    piste: PisteConfig

    def __init__(self, piste_config: PisteConfig):
        """Create configuration from PISTE config."""
        super().__init__(piste=piste_config)
