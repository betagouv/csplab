from dataclasses import dataclass
from uuid import UUID

from domain.entities.offer import Offer


@dataclass
class PublishOfferInput:
    source_id: UUID
    offer: Offer
