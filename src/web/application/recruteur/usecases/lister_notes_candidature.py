from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.entities.note import Note
from domain.recruteur.repositories.note_repository_interface import INoteRepository


@dataclass
class ListerNotesCandidatureQuery:
    candidature_id: UUID


class ListerNotesCandidatureUsecase(IUseCase[ListerNotesCandidatureQuery, list[Note]]):
    def __init__(self, note_repository: INoteRepository):
        self.note_repository = note_repository

    def execute(self, query: ListerNotesCandidatureQuery) -> list[Note]:
        # TODO / BOLA : check requesting user as rights to read candidature notes
        return self.note_repository.list_by_candidature(query.candidature_id)
