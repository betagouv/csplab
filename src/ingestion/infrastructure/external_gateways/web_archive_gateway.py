from domain.gateways.archive_gateway import IArchiveGateway
from infrastructure.external_gateways.base_web_gateway import BaseWebGateway


class WebArchiveGateway(BaseWebGateway, IArchiveGateway):
    async def archive(self, reference: str, source_id: str) -> None:
        await self._post(
            "/offres/archiver",
            json={"reference": reference, "source_id": source_id},
        )
