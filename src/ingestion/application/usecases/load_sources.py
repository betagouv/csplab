import asyncio
import logging

import httpx
from referentiel.entities.source import Source

from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.sources_repository import ISourcesRepository

logger = logging.getLogger(__name__)

# Startup budget of 30 s, an accepted trade-off between tolerating a slow web and
# failing fast. Worst case: 4 × 5 s per attempt + 1 + 2 + 4 s backoff = 27 s.
# The per-attempt timeout bounds the whole request: httpx timeouts apply to each
# network wait, so a response trickling in chunks would never trigger them.
_MAX_ATTEMPTS = 4
_BASE_DELAY_SECONDS = 1.0
_ATTEMPT_TIMEOUT_SECONDS = 5.0
_SERVER_ERROR_STATUS = 500


def _is_transient(exc: httpx.HTTPError | TimeoutError) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= _SERVER_ERROR_STATUS
    return isinstance(exc, httpx.TransportError)


class LoadSourcesUsecase:
    def __init__(
        self,
        sources_gateway: ISourcesGateway,
        repository: ISourcesRepository,
        max_attempts: int = _MAX_ATTEMPTS,
        base_delay_seconds: float = _BASE_DELAY_SECONDS,
        attempt_timeout_seconds: float = _ATTEMPT_TIMEOUT_SECONDS,
    ) -> None:
        self._sources_gateway = sources_gateway
        self._repository = repository
        self._max_attempts = max_attempts
        self._base_delay_seconds = base_delay_seconds
        self._attempt_timeout_seconds = attempt_timeout_seconds

    async def execute(self) -> None:
        sources = await self._fetch_sources_with_retry()
        self._repository.load(sources)
        logger.info("Loaded %d source(s) into repository", len(self._repository))

    async def _fetch_sources_with_retry(self) -> list[Source]:
        attempt = 1
        while True:
            try:
                async with asyncio.timeout(self._attempt_timeout_seconds):
                    return await self._sources_gateway.fetch_sources()
            except (httpx.HTTPError, TimeoutError) as exc:
                if not _is_transient(exc):
                    raise
                if attempt == self._max_attempts:
                    logger.error(
                        "Fetching sources failed after %d attempts: %r", attempt, exc
                    )
                    raise
                delay = self._base_delay_seconds * 2 ** (attempt - 1)
                logger.warning(
                    "Fetching sources failed (attempt %d/%d), retrying in %.1fs: %r",
                    attempt,
                    self._max_attempts,
                    delay,
                    exc,
                )
                await asyncio.sleep(delay)
                attempt += 1
