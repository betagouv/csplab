from datetime import datetime
from typing import Protocol

from domain.entities.raw_offer import RawOffer


class IRawOfferRepository(Protocol):
    async def upsert(self, offer: RawOffer) -> None: ...
    async def mark_as_cleaned(
        self, reference: str, source_id: str, cleaned_at: datetime
    ) -> None: ...
    async def mark_as_upserted(
        self, reference: str, source_id: str, upsert_at: datetime
    ) -> None: ...
