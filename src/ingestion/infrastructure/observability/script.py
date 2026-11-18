import asyncio
from collections.abc import Coroutine
from typing import Any

from api.config import get_settings
from infrastructure.observability.log_config import configure_logging
from infrastructure.observability.sentry import init_sentry


def run_script(coro: Coroutine[Any, Any, None]) -> None:
    """Entry point of the bin/ scripts: logging, Sentry without tracing, then run."""
    configure_logging(get_settings().log_level)
    init_sentry(get_settings(), tracing=False)
    asyncio.run(coro)
