"""Offers repository interface definitions."""

from typing import List, Protocol

from domain.entities.offer import Offer
from domain.repositories.document_repository_interface import IUpsertResult


class IOffersRepository(Protocol):
    """Interface for Offers repository operations."""

    def upsert_batch(self, offers_list: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offers entities and return operation results."""
        ...

    def find_by_id(self, offer_id: int) -> Offer:
        """Find a Offer by its ID."""
        ...
