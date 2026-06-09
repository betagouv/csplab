from typing import List, Protocol
from uuid import UUID

from referentiel.entities.concours import Concours
from referentiel.types import IUpsertResult
from referentiel.value_objects.nor import NOR


class IConcoursRepository(Protocol):
    # todo move this logic in ingestion
    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult: ...

    def get_by_id(self, concours_id: UUID) -> Concours: ...

    def get_by_ids(self, concours_ids: List[UUID]) -> List[Concours]: ...

    def get_by_nor(self, nor: NOR) -> Concours: ...

    def get_all(self) -> List[Concours]: ...

    # todo move this logic in ingestion
    def get_pending_processing(self, limit: int = 1000) -> List[Concours]: ...

    # todo move this logic in ingestion
    def mark_as_processed(self, offers_list: List[Concours]) -> int: ...

    # todo move this logic in ingestion
    def mark_as_pending(self, offers_list: List[Concours]) -> int: ...
