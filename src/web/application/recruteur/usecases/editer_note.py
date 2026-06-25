from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import (
    NoteIntrouvable,
    NoteModificationNonAutorisee,
)
from domain.recruteur.repositories.note_repository_interface import INoteRepository


@dataclass
class EditerNoteCommand:
    candidature_id: UUID
    note_id: UUID
    message: str
    mis_a_jour_par_id: UUID


class EditerNoteUsecase(IUseCase[EditerNoteCommand, Note]):
    def __init__(
        self,
        note_repository: INoteRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.note_repository = note_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: EditerNoteCommand) -> Note:
        note = self.note_repository.get_by_id(command.note_id)
        if note.candidature_id != command.candidature_id:
            raise NoteIntrouvable(command.note_id)
        if note.publie_par_id != command.mis_a_jour_par_id:
            raise NoteModificationNonAutorisee(command.note_id)
        note.modifier_message(
            message=command.message,
            mis_a_jour_par_id=command.mis_a_jour_par_id,
        )
        self.note_repository.save(note)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.mis_a_jour_par_id, aggregate=note
        )
        return note
