from typing import List, Protocol, TypedDict
from uuid import UUID

from referentiel.entities.offer import Offer
from referentiel.repositories.offers_repository_interface import IOffersRepository
from referentiel.types import IUpsertResult


class IArchiveError(TypedDict):
    entity_id: UUID
    error: str
    exception: Exception


class IArchiveResult(TypedDict):
    fetched: int
    vector_deleted: int
    entity_archived: int
    errors: List[IArchiveError]


class IIngestionOffersRepository(IOffersRepository, Protocol):
    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult: ...

    def get_pending_processing(self, limit: int = 1000) -> List[Offer]: ...

    def mark_as_processed(self, offers_list: List[Offer]) -> int: ...

    def mark_as_pending(self, offers_list: List[Offer]) -> int: ...

    def mark_as_archived(self, offers_list: List[Offer]) -> int: ...

    def count_published(self) -> int: ...

    def count_archived(self) -> int: ...
