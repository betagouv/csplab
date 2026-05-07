from fastapi import FastAPI

from api.config import get_settings
from api.routes import public_router


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

    app = FastAPI(title="Ingestion Microservice", version="0.1.0")
    app.include_router(public_router)

    return app


app = create_app()
