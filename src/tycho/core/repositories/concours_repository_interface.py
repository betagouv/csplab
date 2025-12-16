"""Concours repository interface definitions."""

from typing import List, Optional, Protocol

from core.entities.concours import Concours
from core.repositories.document_repository_interface import IUpsertResult


class IConcoursRepository(Protocol):
    """Interface for Concours repository operations."""

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        ...

    def find_by_corps(self, corps: str) -> Optional[Concours]:
        """Find a Concours by its Corps name."""
        ...

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        ...
