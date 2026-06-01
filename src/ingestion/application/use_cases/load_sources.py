import logging

from domain.gateways.sources_gateway import ISourcesGateway
from domain.repositories.sources_repository import ISourcesRepository

logger = logging.getLogger(__name__)


class LoadSourcesUseCase:
    def __init__(
        self,
        sources_gateway: ISourcesGateway,
        repository: ISourcesRepository,
    ) -> None:
        self._sources_gateway = sources_gateway
        self._repository = repository

    async def execute(self) -> None:
        sources = await self._sources_gateway.fetch_sources()
        self._repository.load(sources)
        logger.info("Loaded %d source(s) into repository", len(self._repository))
