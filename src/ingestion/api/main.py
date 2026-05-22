import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.config import get_settings
from api.routes import get_http_client, public_router
from application.use_cases.load_sources import LoadSourcesUseCase
from infrastructure.sources_registry import SourcesRegistry

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

    registry = SourcesRegistry()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if settings.web_base_url and settings.web_api_key:
            async with asynccontextmanager(get_http_client)() as client:
                use_case = LoadSourcesUseCase(
                    client=client,
                    web_base_url=settings.web_base_url,
                    web_api_key=settings.web_api_key,
                    registry=registry,
                )
                await use_case.execute()
        yield

    app = FastAPI(title="Ingestion Microservice", version="0.1.0", lifespan=lifespan)
    app.state.sources_registry = registry
    app.include_router(public_router)

    return app


app = create_app()
