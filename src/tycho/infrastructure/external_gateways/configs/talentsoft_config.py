"""Configuration for Talentsoft external gateway."""

from pydantic import BaseModel, HttpUrl


class TalentsoftGatewayConfig(BaseModel):
    """Configuration for FO Talentsoft gateway."""

    base_url: HttpUrl
    client_id: str
    client_secret: str
