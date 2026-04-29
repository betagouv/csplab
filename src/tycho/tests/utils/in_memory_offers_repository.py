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
    def __init__(self):
        self._offers: Dict[UUID, Offer] = {}
        self._external_id_index: Dict[str, UUID] = {}

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
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

    def get_by_id(self, offer_id: UUID) -> Offer:
        offer = self._offers.get(offer_id)
        if offer is None:
            raise OfferDoesNotExist(str(offer_id))
        return offer

    def get_by_ids(self, offer_ids: List[UUID]) -> List[Offer]:
        return []

    def get_by_external_id(self, external_id: str) -> Offer:
        offer_id = self._external_id_index.get(external_id)
        if offer_id is None:
            raise OfferDoesNotExist(external_id)
        return self._offers[offer_id]

    def get_by_external_ids(selk, external_ids: List[str]) -> List[Offer]:
        return []

    def get_all(self) -> List[Offer]:
        return list(self._offers.values())

    def clear(self) -> None:
        self._offers.clear()
        self._external_id_index.clear()

    def get_pending_processing(self, limit: int = 1000) -> List[Offer]:
        return []

    def mark_as_processed(self, offers_list: List[Offer]) -> int:
        return 0

    def mark_as_pending(self, offers_list: List[Offer]) -> int:
        return 0

    def mark_as_archived(self, offers_list: List[Offer]) -> int:
        return 0
