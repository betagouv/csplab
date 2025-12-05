"""Corps repository interface definitions."""

from typing import List, Optional, Protocol

from core.entities.corps import Corps
from core.repositories.document_repository_interface import IUpsertResult


class ICorpsRepository(Protocol):
    """Interface for Corps repository operations."""

    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult:
        """Insert or update multiple Corps entities and return operation results."""
        ...

    def find_by_id(self, corps_id: int) -> Optional[Corps]:
        """Find a Corps by its ID."""
        ...

    def get_all(self) -> List[Corps]:
        """Get all Corps entities."""
        ...
