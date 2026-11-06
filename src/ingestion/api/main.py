import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from api.config import get_settings
from api.routes import public_router
from infrastructure.di.container import create_container
from infrastructure.observability.log_config import configure_logging
from infrastructure.observability.sentry import init_sentry

configure_logging(get_settings().log_level)

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
