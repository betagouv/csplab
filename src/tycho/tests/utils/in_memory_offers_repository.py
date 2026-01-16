"""In-memory implementation of IOffersRepository for testing purposes."""

from typing import Dict, List, Optional
from uuid import UUID, uuid4

from domain.entities.offer import Offer
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.offers_repository_interface import IOffersRepository


class InMemoryOffersRepository(IOffersRepository):
    """In-memory implementation of IOffersRepository for testing."""

    def __init__(self):
        """Initialize with empty storage."""
        self._offers: Dict[UUID, Offer] = {}

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offers entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for offer in offers_list:
            try:
                if offer.id is None or offer.id not in self._offers:
                    # Create new
                    if offer.id is None:
                        offer.id = uuid4()
                    self._offers[offer.id] = offer
                    created += 1
                else:
                    # Update existing
                    self._offers[offer.id] = offer
                    updated += 1
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": offer.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, offer_id: UUID) -> Optional[Offer]:
        """Find a Offer by its ID."""
        return self._offers.get(offer_id)

    def clear(self) -> None:
        """Clear all stored offers (for testing)."""
        self._offers.clear()
