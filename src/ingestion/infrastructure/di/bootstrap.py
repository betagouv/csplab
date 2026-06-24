import asyncio
from typing import TYPE_CHECKING

from celery.signals import worker_process_init

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
    init_container()
