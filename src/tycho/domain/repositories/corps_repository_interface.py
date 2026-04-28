"""Corps repository interface definitions."""

from typing import List, Protocol
from uuid import UUID

from domain.entities.corps import Corps
from domain.repositories.document_repository_interface import IUpsertResult


class ICorpsRepository(Protocol):
    """Interface for Corps repository operations."""

    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult:
        """Insert or update multiple Corps entities and return operation results."""
        ...

    def get_by_id(self, corps_id: UUID) -> Corps:
        """Get a Corps by its ID."""
        ...

    def get_by_code(self, code: str) -> Corps:
        """Get a Corps by its code."""
        ...

    def get_all(self) -> List[Corps]:
        """Get all Corps entities."""
        ...

    def get_pending_processing(self, limit: int = 1000) -> List[Corps]: ...

    def mark_as_processed(self, offers_list: List[Corps]) -> int: ...

    def mark_as_pending(self, offers_list: List[Corps]) -> int: ...
