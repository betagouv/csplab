from typing import List, Protocol
from uuid import UUID

from referentiel.entities.corps import Corps
from referentiel.types import IUpsertResult


class ICorpsRepository(Protocol):
    # todo move this logic in ingestion
    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult: ...

    def get_by_id(self, corps_id: UUID) -> Corps: ...

    def get_by_code(self, code: str) -> Corps: ...

    def get_all(self) -> List[Corps]: ...

    # todo move this logic in ingestion
    def get_pending_processing(self, limit: int = 1000) -> List[Corps]: ...

    # todo move this logic in ingestion
    def mark_as_processed(self, offers_list: List[Corps]) -> int: ...

    # todo move this logic in ingestion
    def mark_as_pending(self, offers_list: List[Corps]) -> int: ...
