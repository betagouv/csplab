import logging

from application.usecases._fetch_with_retry import (
    ATTEMPT_TIMEOUT_SECONDS,
    BASE_DELAY_SECONDS,
    MAX_ATTEMPTS,
    fetch_with_retry,
)
from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.sources_repository import ISourcesRepository

logger = logging.getLogger(__name__)


class LoadSourcesUsecase:
    def __init__(
        self,
        sources_gateway: ISourcesGateway,
        repository: ISourcesRepository,
        max_attempts: int = MAX_ATTEMPTS,
        base_delay_seconds: float = BASE_DELAY_SECONDS,
        attempt_timeout_seconds: float = ATTEMPT_TIMEOUT_SECONDS,
    ) -> None:
        self._sources_gateway = sources_gateway
        self._repository = repository
        self._max_attempts = max_attempts
        self._base_delay_seconds = base_delay_seconds
        self._attempt_timeout_seconds = attempt_timeout_seconds

    async def execute(self) -> None:
        sources = await fetch_with_retry(
            self._sources_gateway.fetch_sources,
            label="sources",
            max_attempts=self._max_attempts,
            base_delay_seconds=self._base_delay_seconds,
            attempt_timeout_seconds=self._attempt_timeout_seconds,
        )
        self._repository.load(sources)
        logger.info("Loaded %d source(s) into repository", len(self._repository))
