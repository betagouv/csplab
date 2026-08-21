from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    OrganismeRecruteurSansEtapes,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)


class InitRecrutementEtapesUsecase(
    IUseCase[RecrutementRequest, tuple[EtapeRecrutement, ...]]
):
    def __init__(
        self,
        permission_service: OrganismePermissionService,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        recrutement_repository: IRecrutementRepository,
        audit_log_writer: AuditLogWriter,
    ):
        self.permission_service = permission_service
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.recrutement_repository = recrutement_repository
        self.audit_log_writer = audit_log_writer

    def can_execute(
        self, command: RecrutementRequest
    ) -> tuple[OrganismeRecruteur, Recrutement]:
        organisme_recruteur = self.organisme_recruteur_repository.get_by_id(
            command.organisme_id
        )
        if organisme_recruteur.etapes is None:
            raise OrganismeRecruteurSansEtapes(command.organisme_id)
        recrutement = self.recrutement_repository.get_by_id(command.recrutement_id)
        if command.organisme_id != recrutement.organisme_id:
            raise OrganismeRecrutementIncoherents(
                command.organisme_id, command.recrutement_id
            )
        self.permission_service.est_autorise(
            action=OrganismeAction.INIT_RECRUTEMENT_ETAPES,
            organisme_id=command.organisme_id,
            recrutement_id=command.recrutement_id,
            utilisateur=command.utilisateur,
        )
        return organisme_recruteur, recrutement

    def execute(self, command: RecrutementRequest) -> tuple[EtapeRecrutement, ...]:
        organisme_recruteur, recrutement = self.can_execute(command)
        recrutement.reinitialiser_etapes(etapes_organisme=organisme_recruteur.etapes)
        self.recrutement_repository.save(recrutement)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=recrutement
        )
        return recrutement.etapes
