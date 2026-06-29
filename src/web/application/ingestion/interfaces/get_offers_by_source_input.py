from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetOffersBySourceInput:
    source_id: UUID
    utilisateur_entity_id: UUID | None = None
