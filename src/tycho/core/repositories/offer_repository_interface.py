"""Offer repository interface definitions."""

from typing import List, Optional, Protocol
from uuid import UUID

from core.entities.offer import Offer
from core.repositories.document_repository_interface import IUpsertResult


class IOfferRepository(Protocol):
    """Interface for Offer repository operations."""

    def upsert_batch(self, offers: List[Offer]) -> IUpsertResult:
        """Insert or update multiple Offer entities and return operation results."""
        ...

    def find_by_id(self, offer_id: UUID) -> Optional[Offer]:
        """Find an Offer by its ID."""
        ...
