"""In-memory Corps repository implementation for testing."""

from typing import Dict, List, Optional

from core.entities.corps import Corps
from core.repositories.corps_repository_interface import ICorpsRepository


class InMemoryCorpsRepository(ICorpsRepository):
    """In-memory implementation of Corps repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: Dict[int, Corps] = {}

    def save_batch(self, corps: List[Corps]) -> dict:
        """Save a batch of Corps entities and return operation results."""
        created = 0
        updated = 0
        errors = 0

        for corp in corps:
            try:
                if corp.id in self._storage:
                    updated += 1
                else:
                    created += 1
                self._storage[corp.id] = corp
            except Exception:
                errors += 1

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
