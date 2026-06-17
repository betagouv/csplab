from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from domain.audit.services.audit_log_writer import AuditLogWriter
from domain.candidate.entities.candidature import Candidature
from domain.candidate.exceptions.candidature_errors import (
    CandidatureNexistePas,
)
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.candidate.services.candidature_actors_validator import (
    CandidatureActorsValidator,
)


class SubmitApplicationUsecase(
    IUseCase[SubmitApplicationCommand, Candidature],
):
    def __init__(
        self,
        candidature_repository: ICandidatureRepository,
        actors_validator: CandidatureActorsValidator,
        audit_log_writer: AuditLogWriter,
        logger: ILogger,
    ):
        self.logger = logger
        self.candidature_repository = candidature_repository
        self.actors_validator = actors_validator
        self.audit_log_writer = audit_log_writer

    def execute(self, command: SubmitApplicationCommand) -> Candidature:
        self.logger.info(
            "Starting candidature submission for candidate_uuid='%s', offer_uuid=%d",
        )
        offre_id = command.offre_id
        candidat_id = command.candidat_id

        self.actors_validator.validate(candidat_id, offre_id)

        # todo: rbac should manage access:
        # candidate can only get access to its candidatures
        candidature = None
        try:
            candidature = self.candidature_repository.get_by_offer(
                offre_id, candidat_id
            )
        except CandidatureNexistePas as e:
            self.logger.info(e.message)
            candidature = Candidature.create(
                offre_id=offre_id,
                candidat_id=candidat_id,
            )
        # todo entity document
        # add document gate way and repository here
        # candidature.deposer_documents(DocumentsDeposes())

        candidature.soumettre_candidature()
        self.candidature_repository.save(candidature)

        self.audit_log_writer.drain_events(
            utilisateur_id=candidat_id, aggregate=candidature
        )
        return candidature
