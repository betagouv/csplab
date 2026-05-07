import os

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    api_key: str
    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.1
    sentry_traces_sample_rate: float | None = 0.1


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=None)

    api_key: str = "test-api-key-for-development"
    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.0
    sentry_traces_sample_rate: float | None = 0.0


def get_settings() -> Settings:
    """Get settings based on environment."""
    if os.getenv("TESTING", "false").lower() == "true":
        return TestSettings()
    return Settings()


settings = get_settings()
