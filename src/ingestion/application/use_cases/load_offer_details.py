from application.interfaces.talentsoft_client_interface import ITalentsoftFrontClient
from infrastructure.external_gateways.dtos.talentsoft_dtos import TalentsoftDetailOffer


class LoadOfferDetailsUseCase:
    def __init__(self, talentsoft_client: ITalentsoftFrontClient) -> None:
        self._talentsoft_client = talentsoft_client

    async def execute(self, reference: str) -> TalentsoftDetailOffer:
        return await self._talentsoft_client.get_detail(reference)
