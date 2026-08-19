from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.errors.application_errors_recruteur import (
    OrganismeRecrutementIncoherents,
    OrganismeRecruteurSansEtapes,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_repository_interface import (
    IRecrutementRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class InitRecrutementEtapesCommand(RecrutementRequest):
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False


class InitRecrutementEtapesUsecase(
    IUseCase[InitRecrutementEtapesCommand, tuple[EtapeRecrutement, ...]]
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
        self, command: InitRecrutementEtapesCommand
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
            agent_id=command.utilisateur_id,
            recrutement_id=command.recrutement_id,
            est_staff=command.est_staff,
        )
        return organisme_recruteur, recrutement

    def execute(
        self, command: InitRecrutementEtapesCommand
    ) -> tuple[EtapeRecrutement, ...]:
        organisme_recruteur, recrutement = self.can_execute(command)
        recrutement.init_etapes_recrutement(etapes=organisme_recruteur.etapes)
        self.recrutement_repository.save(recrutement)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur_id, aggregate=recrutement
        )
        return recrutement.etapes
