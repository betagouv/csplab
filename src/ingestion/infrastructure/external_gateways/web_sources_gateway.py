from domain.gateways.sources_gateway import ISourcesGateway
from domain.value_objects.source import Source
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway


class WebSourcesGateway(BaseWebGateway, ISourcesGateway):
    async def fetch_sources(self) -> list[Source]:
        response = await self._get("/sources/")
        return [Source(**item) for item in response.json()]
