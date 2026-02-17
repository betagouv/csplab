"""Concours repository interface definitions."""

from typing import List, Protocol
from uuid import UUID

from domain.entities.concours import Concours
from domain.repositories.document_repository_interface import IUpsertResult
from domain.value_objects.nor import NOR


class IConcoursRepository(Protocol):
    """Interface for Concours repository operations."""

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        ...

    def find_by_id(self, concours_id: UUID) -> Concours:
        """Find a Concours by its ID."""
        ...

    def find_by_nor(self, nor: NOR) -> Concours:
        """Find a Concours by its NOR."""
        ...

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        ...
