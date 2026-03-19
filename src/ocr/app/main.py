from fastapi import FastAPI

from app import routes
from app._sentry import sentry_init
from app.config import settings
from app.routes import protected_router, public_router
from infrastructure.di.container import Container

if settings.sentry_dsn:
    sentry_init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        profiles_sample_rate=settings.sentry_profiles_sample_rate,
    )


def create_app():
    container = Container()

    app = FastAPI(title="OCR Microservice", version="0.1.0")
    app.container = container

    container.wire(modules=[routes])

    app.include_router(public_router)
    app.include_router(protected_router)

    return app


app = create_app()
