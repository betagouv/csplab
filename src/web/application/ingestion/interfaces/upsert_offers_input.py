from dataclasses import dataclass
from uuid import UUID

from referentiel.entities.offer import Offer


@dataclass
class UpsertOffersInput:
    source_id: UUID
    offers: list[Offer]
    utilisateur_username: UUID | None = None
