import logging

from application.usecases._fetch_with_retry import (
    ATTEMPT_TIMEOUT_SECONDS,
    BASE_DELAY_SECONDS,
    MAX_ATTEMPTS,
    fetch_with_retry,
)
from domain.gateways.metiers_gateway import IMetiersGateway
from domain.repositories.metiers_multi_domaines_repository import (
    IMetiersMultiDomainesRepository,
)

logger = logging.getLogger(__name__)


class LoadMetiersMultiDomainesUsecase:
    def __init__(
        self,
        metiers_gateway: IMetiersGateway,
        repository: IMetiersMultiDomainesRepository,
        max_attempts: int = MAX_ATTEMPTS,
        base_delay_seconds: float = BASE_DELAY_SECONDS,
        attempt_timeout_seconds: float = ATTEMPT_TIMEOUT_SECONDS,
    ) -> None:
        self._metiers_gateway = metiers_gateway
        self._repository = repository
        self._max_attempts = max_attempts
        self._base_delay_seconds = base_delay_seconds
        self._attempt_timeout_seconds = attempt_timeout_seconds

    async def execute(self) -> None:
        codes = await fetch_with_retry(
            self._metiers_gateway.fetch_metiers_multi_domaines,
            label="metiers",
            max_attempts=self._max_attempts,
            base_delay_seconds=self._base_delay_seconds,
            attempt_timeout_seconds=self._attempt_timeout_seconds,
        )
        self._repository.load(codes)
        logger.info(
            "Loaded %d metier(s) belonging to several domains: %s",
            len(codes),
            ", ".join(sorted(codes)),
        )
