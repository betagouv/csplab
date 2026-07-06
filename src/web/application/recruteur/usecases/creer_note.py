from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.candidate.exceptions.candidature_errors import CandidatureIntrouvable
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
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
        candidature_repository: ICandidatureRepository,
        agent_repository: IAgentRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.note_repository = note_repository
        self.candidature_repository = candidature_repository
        self.agent_repository = agent_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: CreerNoteCommand) -> Note:
        if not self.candidature_repository.exists(command.candidature_id):
            raise CandidatureIntrouvable(command.candidature_id)
        if not self.agent_repository.exists(command.publie_par_id):
            raise ProfilAgentNexistePas(command.publie_par_id)

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
