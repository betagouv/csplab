from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    sentry_dsn: HttpUrl | None = None
    sentry_profiles_sample_rate: float | None = 0.1
    sentry_traces_sample_rate: float | None = 0.1

    class Config:
        env_file = ".env"


settings = Settings()
