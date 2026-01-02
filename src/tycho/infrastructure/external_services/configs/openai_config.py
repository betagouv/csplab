"""Configuration for shared services."""

from pydantic import BaseModel, HttpUrl


class OpenAIConfig(BaseModel):
    """Configuration for OpenAI API client."""

    api_key: str
    base_url: HttpUrl
    model: str


class OpenAIServiceConfig(BaseModel):
    """Configuration for shared services."""

    openai: OpenAIConfig

    def __init__(self, openai_config: OpenAIConfig):
        """Create configuration from OpenAI config."""
        super().__init__(openai=openai_config)
