from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.note import Note
from domain.recruteur.errors.note_errors import NoteIntrouvable
from domain.recruteur.repositories.note_repository_interface import INoteRepository


@dataclass
class SupprimerNoteCommand:
    note_id: UUID
    supprime_par_id: UUID


class SupprimerNoteUsecase(IUsecase[SupprimerNoteCommand, None]):
    def __init__(
        self,
        note_repository: INoteRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.note_repository = note_repository
        self.audit_log_writer = audit_log_writer

    def can_execute(self, command: SupprimerNoteCommand) -> Note:
        note = self.note_repository.get_by_id(command.note_id)
        if note.publie_par_id != command.supprime_par_id:
            raise NoteIntrouvable(command.note_id)
        return note

    def execute(self, command: SupprimerNoteCommand) -> None:
        note = self.can_execute(command)

        note.supprimer()
        self.note_repository.delete(note.entity_id)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.supprime_par_id, aggregate=note
        )
