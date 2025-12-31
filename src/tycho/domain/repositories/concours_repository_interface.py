"""Concours repository interface definitions."""

from typing import List, Optional, Protocol

from domain.entities.concours import Concours
from domain.repositories.document_repository_interface import IUpsertResult


class IConcoursRepository(Protocol):
    """Interface for Concours repository operations."""

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        ...

    def find_by_id(self, concours_id: int) -> Optional[Concours]:
        """Find a Concours by its ID."""
        ...

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        ...
