from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)


class InitRecrutementEtapesUsecase(
    IUsecase[RecrutementRequest, tuple[EtapeRecrutement, ...]]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        recrutement_repository: IRecrutementRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.recrutement_repository = recrutement_repository
        self.audit_log_writer = audit_log_writer

    def execute(self, command: RecrutementRequest) -> tuple[EtapeRecrutement, ...]:
        organisme_recruteur = self.organisme_recruteur_repository.get_by_id(
            command.organisme_id
        )
        recrutement = self.recrutement_repository.get_by_id(command.recrutement_id)
        if command.organisme_id != recrutement.organisme_id:
            raise OrganismeRecrutementIncoherents(
                command.organisme_id, command.recrutement_id
            )

        # Perf: can_execute() re-checks organisme/recrutement existence already
        # proven by the repository fetches above — dedupe when this usecase
        # migrates to ADR-009.
        can_execute(
            action=OrganismeAction.INIT_RECRUTEMENT_ETAPES,
            organisme_id=command.organisme_id,
            recrutement_id=command.recrutement_id,
            utilisateur=command.utilisateur,
        )

        recrutement.reinitialiser_etapes(etapes_organisme=organisme_recruteur.etapes)
        self.recrutement_repository.save(recrutement)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=recrutement
        )
        return recrutement.etapes
