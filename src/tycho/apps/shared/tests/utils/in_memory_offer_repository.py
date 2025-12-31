"""In-memory Offer repository implementation for testing."""

from typing import Dict, List, Optional

from core.entities.offer import Offer
from core.repositories.document_repository_interface import IUpsertError, IUpsertResult
from core.repositories.offer_repository_interface import IOfferRepository


class InMemoryOfferRepository(IOfferRepository):
    """In-memory implementation of Offer repository for testing."""

    def __init__(self) -> None:
        """Initialize with empty storage."""
        self._storage: Dict[int, Offer] = {}

    def upsert_batch(self, offers: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offer entities and return operation results."""
        created = 0
        updated = 0
        errors: List[IUpsertError] = []

        for offer in offers:
            try:
                if offer.id in self._storage:
                    updated += 1
                else:
                    created += 1
                self._storage[offer.id] = offer
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": offer.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {
            "created": created,
            "updated": updated,
            "errors": errors,
        }

    def find_by_id(self, offer_id: int) -> Optional[Offer]:
        """Find an Offer by its ID."""
        return self._storage.get(offer_id)

    def get_all(self) -> List[Offer]:
        """Get all Offer entities."""
        return list(self._storage.values())

    def clear(self) -> None:
        """Clear all stored entities (for testing)."""
        self._storage.clear()
