from uuid import UUID

from domain.gateways.offers_by_source_gateway import IOffersBySourceGateway
from infrastructure.external_gateways.base_web_gateway import (
    _API_PREFIX,
    BaseWebGateway,
)


class WebOffersBySourceGateway(BaseWebGateway, IOffersBySourceGateway):
    async def fetch_references(self, source_id: UUID) -> list[str]:
        url: str | None = f"{self._base_url}{_API_PREFIX}/offres/sources/{source_id}"
        references: list[str] = []

        while url:
            response = await self._client.get(url, headers=self._auth_headers)
            response.raise_for_status()
            data = response.json()
            references.extend(item["reference"] for item in data["results"])
            url = data["next"]

        return references
