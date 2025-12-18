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


class TalentSoftConfig(BaseModel):
    """Configuration for TalentSoft API client."""

    base_url: HttpUrl
    api_key: str


class IngestionConfig(BaseModel):
    """Configuration for ingestion app."""

    piste: PisteConfig
    talentsoft: TalentSoftConfig

    def __init__(self, piste_config: PisteConfig, talentsoft_config: TalentSoftConfig):
        """Create configuration from PISTE and TalentSoft configs."""
        super().__init__(piste=piste_config, talentsoft=talentsoft_config)
