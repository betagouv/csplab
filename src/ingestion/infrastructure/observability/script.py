import asyncio
import logging
from collections.abc import Coroutine
from typing import Any

from api.config import get_settings
from infrastructure.observability.sentry import init_sentry


def run_script(coro: Coroutine[Any, Any, None]) -> None:
    """Entry point of the bin/ scripts: logging, Sentry without tracing, then run."""
    logging.basicConfig(level=logging.INFO)
    init_sentry(get_settings(), tracing=False)
    asyncio.run(coro)
