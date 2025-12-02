"""In-memory Corps repository implementation for testing."""

from typing import Dict, List, Optional

from core.entities.corps import Corps
from core.repositories.corps_repository_interface import ICorpsRepository
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult


class InMemoryCorpsRepository(ICorpsRepository):
    """In-memory implementation of Corps repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: Dict[int, Corps] = {}

    def upsert(self, corps: Corps) -> Corps:
        """Insert or update a single Corps entity."""
        self._storage[corps.id] = corps
        return corps

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

    def find_by_id(self, corps_id: int) -> Optional[Corps]:
        """Find a Corps by its ID."""
        return self._storage.get(corps_id)

    def clear(self) -> None:
        """Clear all stored entities (for testing)."""
        self._storage.clear()
