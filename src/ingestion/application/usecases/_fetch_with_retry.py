import asyncio
import logging
from collections.abc import Awaitable, Callable

import httpx

logger = logging.getLogger(__name__)

# Startup budget of 30 s, an accepted trade-off between tolerating a slow web and
# failing fast. Worst case: 4 × 5 s per attempt + 1 + 2 + 4 s backoff = 27 s.
# The per-attempt timeout bounds the whole request: httpx timeouts apply to each
# network wait, so a response trickling in chunks would never trigger them.
MAX_ATTEMPTS = 4
BASE_DELAY_SECONDS = 1.0
ATTEMPT_TIMEOUT_SECONDS = 5.0
_SERVER_ERROR_STATUS = 500


def _is_transient(exc: httpx.HTTPError | TimeoutError) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= _SERVER_ERROR_STATUS
    return isinstance(exc, httpx.TransportError)


async def fetch_with_retry[T](
    fetch: Callable[[], Awaitable[T]],
    label: str,
    max_attempts: int,
    base_delay_seconds: float,
    attempt_timeout_seconds: float,
) -> T:
    attempt = 1
    while True:
        try:
            async with asyncio.timeout(attempt_timeout_seconds):
                return await fetch()
        except (httpx.HTTPError, TimeoutError) as exc:
            if not _is_transient(exc):
                raise
            if attempt == max_attempts:
                logger.error(
                    "Fetching %s failed after %d attempts: %r", label, attempt, exc
                )
                raise
            delay = base_delay_seconds * 2 ** (attempt - 1)
            logger.warning(
                "Fetching %s failed (attempt %d/%d), retrying in %.1fs: %r",
                label,
                attempt,
                max_attempts,
                delay,
                exc,
            )
            await asyncio.sleep(delay)
            attempt += 1
