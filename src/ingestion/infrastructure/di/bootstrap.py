import asyncio
from typing import TYPE_CHECKING

import sentry_sdk
from celery.signals import worker_process_init
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

from api.config import settings

if TYPE_CHECKING:
    from infrastructure.di.container import Container

_state: dict[str, "Container | None"] = {"container": None}


def init_container() -> None:
    from infrastructure.di.container import create_container  # noqa: PLC0415

    container = create_container()
    asyncio.run(container.load_sources_use_case().execute())
    _state["container"] = container


def get_container() -> "Container":
    if _state["container"] is None:
        init_container()
    container = _state["container"]
    if container is None:
        raise RuntimeError("Container could not be initialized")
    return container


@worker_process_init.connect
def _init_worker_container(**kwargs: object) -> None:
    if settings.sentry_dsn and str(settings.sentry_dsn).strip():
        sentry_sdk.init(
            dsn=str(settings.sentry_dsn),
            integrations=[
                LoggingIntegration(),
                CeleryIntegration(),
                HttpxIntegration(),
            ],
            traces_sample_rate=settings.sentry_traces_sample_rate,
            profiles_sample_rate=settings.sentry_profiles_sample_rate,
        )
    init_container()
