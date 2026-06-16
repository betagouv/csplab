import asyncio

from celery import Celery
from celery.signals import worker_process_init

from api.config import settings
from infrastructure.di.container import Container, create_container

_state: dict[str, Container | None] = {"container": None}


def init_container() -> None:
    container = create_container()
    asyncio.run(container.load_sources_use_case().execute())
    _state["container"] = container


def get_container() -> Container:
    if _state["container"] is None:
        init_container()
    container = _state["container"]
    if container is None:
        raise RuntimeError("Container could not be initialized")
    return container


@worker_process_init.connect
def _init_worker_container(**kwargs: object) -> None:
    init_container()


def create_celery_app() -> Celery:
    app = Celery("ingestion")
    app.conf.update(
        broker_url=settings.redis_url,
        result_backend=None,
        task_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        include=["application.tasks.process_webhook"],
    )
    return app


celery_app = create_celery_app()
