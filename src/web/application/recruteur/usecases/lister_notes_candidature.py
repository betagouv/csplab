from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.services.note_query_service_interface import (
    INoteQueryService,
    NoteReadModel,
)


@dataclass
class ListerNotesCandidatureQuery:
    candidature_id: UUID


class ListerNotesCandidatureUsecase(
    IUseCase[ListerNotesCandidatureQuery, list[NoteReadModel]]
):
    def __init__(self, note_query_service: INoteQueryService):
        self.note_query_service = note_query_service

    def execute(self, query: ListerNotesCandidatureQuery) -> list[NoteReadModel]:
        return self.note_query_service.get_by_candidature(query.candidature_id)
