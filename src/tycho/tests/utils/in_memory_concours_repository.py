"""In-memory implementation of IConcoursRepository for testing purposes."""

from typing import Dict, List
from uuid import UUID

from domain.entities.concours import Concours
from domain.exceptions.concours_errors import ConcoursDoesNotExist
from domain.repositories.concours_repository_interface import IConcoursRepository
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)


class InMemoryConcoursRepository(IConcoursRepository):
    """In-memory implementation of IConcoursRepository for testing."""

    def __init__(self):
        """Initialize with empty storage."""
        self._concours: Dict[UUID, Concours] = {}

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for concours in concours_list:
            try:
                if concours.id in self._concours:
                    updated += 1
                else:
                    created += 1
                self._concours[concours.id] = concours
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": concours.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, concours_id: UUID) -> Concours:
        """Find a Concours by its ID."""
        if concours_id not in self._concours:
            raise ConcoursDoesNotExist(str(concours_id))
        return self._concours[concours_id]

    def find_by_nor(self, nor) -> Concours:
        """Find a Concours by its NOR."""
        for concours in self._concours.values():
            if concours.nor_original == nor:
                return concours
        raise ConcoursDoesNotExist(str(nor))

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        return list(self._concours.values())

    def clear(self) -> None:
        """Clear all stored concours (for testing)."""
        self._concours.clear()
