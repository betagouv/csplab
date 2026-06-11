import os

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.1
    sentry_traces_sample_rate: float | None = 0.1

    talentsoft_front_client_id: str | None = None
    talentsoft_front_client_secret: str | None = None
    talentsoft_front_base_url: str | None = None

    talentsoft_back_client_id: str | None = None
    talentsoft_back_client_secret: str | None = None
    talentsoft_back_base_url: str | None = None

    web_base_url: str | None = None
    web_api_key: str | None = None

    database_url: str | None = None
    redis_url: str | None = None

    log_level: str = "INFO"
    flower_port: int | None = None


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=None)

    sentry_profiles_sample_rate: float | None = 0.0
    sentry_traces_sample_rate: float | None = 0.0


def get_settings() -> Settings:
    """Get settings based on environment."""
    if os.getenv("TESTING", "false").lower() == "true":
        return TestSettings()
    return Settings()


settings = get_settings()
