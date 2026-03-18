from fastapi import FastAPI

from app._sentry import sentry_init
from app.config import settings
from app.routes import protected_router, public_router

if settings.sentry_dsn:
    from app._sentry import sentry_init

    sentry_init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        profiles_sample_rate=settings.sentry_profiles_sample_rate,
    )

app = FastAPI(title="OCR Microservice", version="0.1.0")

app.include_router(public_router)
app.include_router(protected_router)
