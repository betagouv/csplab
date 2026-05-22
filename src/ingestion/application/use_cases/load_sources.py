import logging

import httpx

from application.interfaces.sources_registry import ISourcesRegistry
from domain.source import Source

logger = logging.getLogger(__name__)


class LoadSourcesUseCase:
    def __init__(
        self,
        client: httpx.AsyncClient,
        web_base_url: str,
        web_api_key: str,
        registry: ISourcesRegistry,
    ) -> None:
        self._client = client
        self._web_base_url = web_base_url
        self._web_api_key = web_api_key
        self._registry = registry

    async def execute(self) -> None:
        url = f"{self._web_base_url}/api/data/sources/"
        response = await self._client.get(
            url,
            headers={"Authorization": f"Api-Key {self._web_api_key}"},
        )
        response.raise_for_status()
        sources = [Source(**item) for item in response.json()]
        self._registry.load(sources)
        logger.info("Loaded %d source(s) into registry", len(self._registry))
