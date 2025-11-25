"""Corps repository interface definitions."""

from typing import List, Optional, Protocol

from core.entities.corps import Corps


class ICorpsRepository(Protocol):
    """Interface for Corps repository operations."""

    def save_batch(self, corps: List[Corps]) -> dict:
        """Save a batch of Corps entities and return operation results."""
        ...

    def find_by_id(self, corps_id: int) -> Optional[Corps]:
        """Find a Corps by its ID."""
        ...
