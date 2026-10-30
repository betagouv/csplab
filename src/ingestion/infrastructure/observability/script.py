import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

from api.config import get_settings
from infrastructure.observability.sentry import init_sentry


def run_script(coro: Coroutine[Any, Any, None]) -> None:
    """Entry point of the bin/ scripts: logging, Sentry without tracing, then run.

    Unhandled errors are reported by the default Sentry integrations, and the
    queue is flushed at exit, so short-lived scripts don't lose their events.
    """
    logging.basicConfig(level=logging.INFO)
    init_sentry(get_settings(), tracing=False)
    asyncio.run(coro)
