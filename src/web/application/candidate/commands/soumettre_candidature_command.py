from dataclasses import dataclass
from uuid import UUID


@dataclass
class SoumettreCandidatureCommand:
    offre_id: UUID
    candidat_id: UUID
