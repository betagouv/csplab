from fastapi import FastAPI

from api import routes
from api.config import get_settings
from api.routes import protected_router, public_router
from infrastructure.di.container import Container


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

    app = FastAPI(title="OCR Microservice", version="0.1.0")
    app.container = container

    container.wire(modules=[routes])

    app.include_router(public_router)
    app.include_router(protected_router)

    return app


app = create_app()
