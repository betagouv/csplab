from dataclasses import dataclass
from uuid import UUID


@dataclass(kw_only=True)
class RecrutementRequest:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False
