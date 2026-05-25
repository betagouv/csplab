from typing import Protocol

from infrastructure.external_gateways.dtos.talentsoft_dtos import TalentsoftDetailOffer


class ITalentsoftFrontClient(Protocol):
    async def get_detail(self, reference: str) -> TalentsoftDetailOffer: ...
