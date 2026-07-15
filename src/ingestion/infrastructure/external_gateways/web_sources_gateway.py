from uuid import UUID

from referentiel.entities.source import Source
from referentiel.value_objects.source_type import SourceType

from domain.gateways.sources_gateway import ISourcesGateway
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway


class WebSourcesGateway(BaseWebGateway, ISourcesGateway):
    async def fetch_sources(self) -> list[Source]:
        response = await self._get("/sources")
        return [
            Source(
                **{
                    **item,
                    "source_id": UUID(item["source_id"]),
                    "type": SourceType(item["type"]),
                }
            )
            for item in response.json()
            if item["type"] == SourceType.TALENTSOFT.value
        ]
