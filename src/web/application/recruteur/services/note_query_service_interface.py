from typing import Protocol
from uuid import UUID

from application.recruteur.dtos.note_read_models import NoteReadModel


class INoteQueryService(Protocol):
    def get_by_candidature(self, candidature_id: UUID) -> list[NoteReadModel]: ...
