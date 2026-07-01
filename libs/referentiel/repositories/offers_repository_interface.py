from typing import List, Protocol
from uuid import UUID

from ddd.page_interface import IPage

from referentiel.entities.offer import Offer


class IOffersRepository(Protocol):
    def get_by_id(self, offer_id: UUID) -> Offer: ...

    def get_by_ids(self, offer_ids: List[UUID]) -> List[Offer]: ...

    def get_by_external_id(self, external_id: str) -> Offer: ...

    def get_by_reference_and_source_id(
        self, reference: str, source_id: UUID
    ) -> Offer: ...

    def get_by_external_ids(self, external_ids: List[str]) -> List[Offer]: ...

    def get_all(self) -> List[Offer]: ...

    def get_filtered(
        self, active: bool, external_id_contains: str | None
    ) -> IPage[Offer]: ...

    def get_by_source_id(self, source_id: UUID) -> IPage[Offer]: ...
