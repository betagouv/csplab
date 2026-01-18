"""Configuration for Talentsoft external gateway."""

from pydantic import BaseModel, HttpUrl


class TalentsoftConfig(BaseModel):
    """Configuration for FO Talentsoft API client."""

    base_url: HttpUrl
    client_id: str
    client_secret: str


class TalentsoftGatewayConfig(BaseModel):
    """Configuration for FO Talentsoft gateway."""

    talentsoft: TalentsoftConfig

    def __init__(self, talentsoft_config: TalentsoftConfig):
        """Create configuration from Talentsoft config."""
        super().__init__(talentsoft=talentsoft_config)
