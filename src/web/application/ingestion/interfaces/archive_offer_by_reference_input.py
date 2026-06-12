from dataclasses import dataclass
from uuid import UUID


@dataclass
class ArchiveOfferByReferenceInput:
    reference: str
    source_id: UUID
    utilisateur_entity_id: UUID | None = None
