from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository

from domain.recruteur.entities.note import Note


class INoteRepository(IBaseRepository[Note], Protocol):
    def list_by_candidature(self, candidature_id: UUID) -> list[Note]: ...
