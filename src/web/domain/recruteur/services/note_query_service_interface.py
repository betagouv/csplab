from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class NoteReadModel:
    entity_id: UUID
    candidature_id: UUID
    message: str
    publie_par_id: UUID
    publie_par_prenom: str
    publie_par_nom: str
    publie_le: datetime


class INoteQueryService(Protocol):
    def list_for_candidature(self, candidature_id: UUID) -> list[NoteReadModel]: ...
