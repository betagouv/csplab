import os

from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.1
    sentry_traces_sample_rate: float | None = 0.1

    class Config:
        env_file = ".env"


class TestSettings(Settings):
    api_key: str = "test-api-key-for-development"
    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.0
    sentry_traces_sample_rate: float | None = 0.0

    class Config:
        env_file = None  # Don't load from .env in tests


def get_settings() -> Settings:
    """Get settings based on environment."""
    if os.getenv("TESTING", "false").lower() == "true":
        return TestSettings()
    return Settings()


settings = get_settings()
