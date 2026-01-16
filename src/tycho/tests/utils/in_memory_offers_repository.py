"""In-memory implementation of IOffersRepository for testing purposes."""

from typing import Dict, List

from domain.entities.offer import Offer
from domain.exceptions.offer_errors import OfferDoesNotExist
from domain.repositories.document_repository_interface import (
    IUpsertError,
    IUpsertResult,
)
from domain.repositories.offers_repository_interface import IOffersRepository


class InMemoryOffersRepository(IOffersRepository):
    """In-memory implementation of IOffersRepository for testing."""

    def __init__(self):
        """Initialize with empty storage."""
        self._offers: Dict[int, Offer] = {}
        self._next_id = 1

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offers entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for offer in offers_list:
            try:
                if offer.id == 0 or offer.id not in self._offers:
                    # Create new
                    if offer.id == 0:
                        offer.id = self._next_id
                        self._next_id += 1
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

    def find_by_id(self, offer_id: int) -> Offer:
        """Find a Offer by its ID."""
        offer = self._offers.get(offer_id)
        if offer is None:
            raise OfferDoesNotExist(offer_id)
        return offer

    def clear(self) -> None:
        """Clear all stored offers (for testing)."""
        self._offers.clear()
        self._next_id = 1
