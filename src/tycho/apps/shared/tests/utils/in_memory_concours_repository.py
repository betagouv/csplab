"""In-memory implementation of IConcoursRepository for testing purposes."""

from typing import Dict, List, Optional

from core.entities.concours import Concours
from core.repositories.concours_repository_interface import IConcoursRepository
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult


class InMemoryConcoursRepository(IConcoursRepository):
    """In-memory implementation of IConcoursRepository for testing."""

    def __init__(self):
        """Initialize with empty storage."""
        self._concours: Dict[int, Concours] = {}
        self._next_id = 1

    def upsert_batch(self, concours_list: List[Concours]) -> IUpsertResult:
        """Insert or update multiple Concours entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for concours in concours_list:
            try:
                if concours.id == 0 or concours.id not in self._concours:
                    # Create new
                    if concours.id == 0:
                        concours.id = self._next_id
                        self._next_id += 1
                    self._concours[concours.id] = concours
                    created += 1
                else:
                    # Update existing
                    self._concours[concours.id] = concours
                    updated += 1
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": concours.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_corps_id(self, corps_id: int) -> Optional[Concours]:
        """Find a Concours by its Corps ID."""
        for concours in self._concours.values():
            if concours.corps_id == corps_id:
                return concours
        return None

    def get_all(self) -> List[Concours]:
        """Get all Concours entities."""
        return list(self._concours.values())

    def find_by_id(self, concours_id: int) -> Optional[Concours]:
        """Find a Concours by its ID."""
        return self._concours.get(concours_id)

    def clear(self) -> None:
        """Clear all stored concours (for testing)."""
        self._concours.clear()
        self._next_id = 1
