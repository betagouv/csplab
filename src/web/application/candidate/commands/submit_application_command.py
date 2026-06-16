from dataclasses import dataclass
from uuid import UUID


@dataclass
class SubmitApplicationCommand:
    offre_id: UUID
    candidat_id: UUID
