"""In-memory Corps repository implementation for testing."""

from typing import Dict, List
from uuid import UUID

from domain.entities.corps import Corps
from domain.exceptions.corps_errors import CorpsDoesNotExist
from domain.repositories.corps_repository_interface import ICorpsRepository
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)


class InMemoryCorpsRepository(ICorpsRepository):
    """In-memory implementation of Corps repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: Dict[UUID, Corps] = {}

    def upsert_batch(self, corps: List[Corps]) -> IUpsertResult:
        """Insert or update multiple Corps entities and return operation results."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for corp in corps:
            try:
                if corp.id in self._storage:
                    updated += 1
                else:
                    created += 1
                self._storage[corp.id] = corp
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": corp.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def find_by_id(self, corps_id: UUID) -> Corps:
        """Find a Corps by its ID."""
        if corps_id not in self._storage:
            raise CorpsDoesNotExist(corps_id)
        return self._storage[corps_id]

    def find_by_code(self, code: str) -> Corps:
        """Find a Corps by its code."""
        for corps in self._storage.values():
            if corps.code == code:
                return corps
        raise CorpsDoesNotExist(code)

    def get_all(self) -> List[Corps]:
        """Get all Corps entities."""
        return list(self._storage.values())

    def clear(self) -> None:
        """Clear all stored entities (for testing)."""
        self._storage.clear()
