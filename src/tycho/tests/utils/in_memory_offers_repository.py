"""In-memory implementation of IOffersRepository for testing purposes."""

from typing import Dict, List
from uuid import UUID

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
        self._offers: Dict[UUID, Offer] = {}
        self._external_id_index: Dict[str, UUID] = {}

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offers entities and return operation results."""
        created = 0
        updated = 0
        errors = []

        for offer in offers_list:
            try:
                if offer.id not in self._offers:
                    # Create new
                    self._offers[offer.id] = offer
                    self._external_id_index[offer.external_id] = offer.id
                    created += 1
                else:
                    # Update existing
                    self._offers[offer.id] = offer
                    self._external_id_index[offer.external_id] = offer.id
                    updated += 1
            except Exception as e:
                error_detail: IUpsertError = {
                    "entity_id": offer.id,
                    "error": str(e),
                    "exception": e,
                }
                errors.append(error_detail)

        return {"created": created, "updated": updated, "errors": errors}

    def find_by_id(self, offer_id: UUID) -> Offer:
        """Find a Offer by its ID."""
        offer = self._offers.get(offer_id)
        if offer is None:
            raise OfferDoesNotExist(str(offer_id))
        return offer

    def find_by_external_id(self, external_id: str) -> Offer:
        """Find an Offer by its external ID (Talentsoft ID)."""
        offer_id = self._external_id_index.get(external_id)
        if offer_id is None:
            raise OfferDoesNotExist(external_id)
        return self._offers[offer_id]

    def get_all(self) -> List[Offer]:
        """Get all Offer entities."""
        return list(self._offers.values())

    def clear(self) -> None:
        """Clear all stored offers (for testing)."""
        self._offers.clear()
        self._external_id_index.clear()
