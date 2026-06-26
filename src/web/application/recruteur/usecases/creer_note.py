from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.note import Note
from domain.recruteur.repositories.note_repository_interface import INoteRepository


@dataclass
class CreerNoteCommand:
    candidature_id: UUID
    publie_par_id: UUID
    message: str


class CreerNoteUsecase(IUseCase[CreerNoteCommand, Note]):
    def __init__(
        self,
        note_repository: INoteRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.note_repository = note_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: CreerNoteCommand) -> Note:
        # TODO / BOLA : check requesting user as rights to add a note to candidature
        note = Note.create(
            candidature_id=command.candidature_id,
            publie_par_id=command.publie_par_id,
            message=command.message,
        )
        self.note_repository.create(note)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.publie_par_id, aggregate=note
        )
        return note
