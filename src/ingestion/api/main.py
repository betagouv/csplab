import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.config import get_settings
from api.routes import public_router
from infrastructure.di.container import create_container
from infrastructure.observability.sentry import init_sentry

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

logger = logging.getLogger(__name__)


def create_app():
    # Get settings dynamically to allow test environment override
    settings = get_settings()

    init_sentry(
        settings,
        [CeleryIntegration(), StarletteIntegration(), FastApiIntegration()],
        tracing=True,
    )

    container = create_container()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        usecase = container.load_sources_usecase()
        await usecase.execute()

        yield

        container.db_engine().dispose()
        await container.http_client().aclose()

    app = FastAPI(title="Ingestion Microservice", version="0.1.0", lifespan=lifespan)
    app.state.container = container
    app.include_router(public_router)

    return app


app = create_app()
