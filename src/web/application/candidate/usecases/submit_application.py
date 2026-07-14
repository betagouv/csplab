from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase

from application.candidate.commands.submit_application_command import (
    SubmitApplicationCommand,
)
from domain.candidate.entities.candidature import Candidature
from domain.candidate.exceptions.candidature_errors import CandidatureDejaSoumise
from domain.candidate.repositories.candidature_repository_interface import (
    ICandidatureRepository,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.repositories.candidat_repository_interface import (
    ICandidatRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)


class SubmitApplicationUsecase(
    IUseCase[SubmitApplicationCommand, Candidature],
):
    def __init__(
        self,
        candidat_repository: ICandidatRepository,
        candidature_repository: ICandidatureRepository,
        recrutement_repository: IRecrutementRepository,
        audit_log_writer: AuditLogWriter,
        logger: ILogger,
    ):
        self.logger = logger
        self.candidat_repository = candidat_repository
        self.candidature_repository = candidature_repository
        self.recrutement_repository = recrutement_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: SubmitApplicationCommand) -> Candidature:
        self.logger.info(
            "Starting candidature submission for candidate_uuid='%s', offer_uuid=%d",
        )
        # todo: rbac should manage access and existence:
        self.candidat_repository.get_by_id(command.candidat_id)
        self.recrutement_repository.get_by_id(command.offre_id)

        if self.candidature_repository.exists_by_candidat_and_offre(
            command.candidat_id, command.offre_id
        ):
            raise CandidatureDejaSoumise(command.candidat_id, command.offre_id)

        candidature = Candidature.create(
            offre_id=command.offre_id,
            candidat_id=command.candidat_id,
        )
        candidature.soumettre_candidature()

        self.candidature_repository.save(candidature)

        self.audit_log_writer.drain_events(
            utilisateur_id=command.candidat_id, aggregate=candidature
        )
        return candidature
