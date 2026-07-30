from typing import List, Optional, Protocol
from uuid import UUID

from ddd.page_interface import IPage

from referentiel.entities.offer import Offer
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.verse import Verse


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
        self,
        active: bool,
        external_id_contains: str | None,
        category: Optional[List[Category]] = None,
        verse: Optional[List[Verse]] = None,
        contract_type: Optional[List[ContractType]] = None,
        experience_level: Optional[List[ExperienceLevel]] = None,
    ) -> IPage[Offer]: ...

    def get_by_source_id(self, source_id: UUID) -> IPage[Offer]: ...
