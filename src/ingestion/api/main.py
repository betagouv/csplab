import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import get_settings
from api.routes import public_router
from infrastructure.di.container import Container

_SKIP_LOG_ATTRS = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message",
    "asctime",
    "exc_text",
}


class _PlaintextFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        extras = {k: v for k, v in record.__dict__.items() if k not in _SKIP_LOG_ATTRS}
        pairs = " ".join(f"{k}={v}" for k, v in extras.items())
        extra_str = f" {pairs}" if pairs else ""
        line = f"{record.levelname} {record.name}: {record.getMessage()}{extra_str}"
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


_handler = logging.StreamHandler()
_handler.setFormatter(_PlaintextFormatter())
logging.basicConfig(level=get_settings().log_level.upper(), handlers=[_handler])


def create_app():
    # Get settings dynamically to allow test environment override
    settings = get_settings()

    if settings.sentry_dsn and str(settings.sentry_dsn).strip():
        from api._sentry import sentry_init  # noqa

        sentry_init(
            dsn=str(settings.sentry_dsn),
            traces_sample_rate=settings.sentry_traces_sample_rate,
            profiles_sample_rate=settings.sentry_profiles_sample_rate,
        )

    container = Container()
    container.config.web_base_url.from_value(settings.web_base_url)
    container.config.web_api_key.from_value(settings.web_api_key)
    container.config.talentsoft_credentials.from_value(
        [
            (client_id, secret)
            for client_id, secret in [
                (
                    settings.talentsoft_back_client_id,
                    settings.talentsoft_back_client_secret,
                ),
            ]
            if client_id and secret
        ]
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.web_base_url and settings.web_api_key:
            use_case = container.load_sources_use_case()
            await use_case.execute()
        yield
        await container.http_client().aclose()

    app = FastAPI(title="Ingestion Microservice", version="0.1.0", lifespan=lifespan)
    app.state.container = container
    app.include_router(public_router)

    return app


app = create_app()
