from dataclasses import dataclass
from uuid import UUID

from referentiel.entities.offer import Offer


@dataclass
class UpsertOffersInput:
    offers: list[Offer]
    utilisateur_entity_id: UUID | None = None
