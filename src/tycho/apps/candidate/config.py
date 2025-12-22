"""Configuration for candidate app."""

from pydantic import BaseModel, HttpUrl


class AlbertConfig(BaseModel):
    """Configuration for Albert API client."""

    api_base_url: HttpUrl
    api_key: str
    model_name: str = "albert-large"
    dpi: int = 200


class CandidateConfig(BaseModel):
    """Configuration for candidate app."""

    albert: AlbertConfig

    def __init__(self, albert_config: AlbertConfig):
        """Create configuration from Albert config."""
        super().__init__(albert=albert_config)
