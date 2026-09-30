from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)


@dataclass
class InitializeOrganismeStepsCommand:
    organisme_id: UUID
    utilisateur: Utilisateur


class InitializeOrganismeStepsUsecase(
    IUsecase[InitializeOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        organisme_permission_service: OrganismePermissionService,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.organisme_permission_service = organisme_permission_service
        self.audit_log_writer = audit_log_writer

    def execute(self, command: InitializeOrganismeStepsCommand) -> OrganismeRecruteur:
        self.organisme_permission_service.can_execute(
            action=OrganismeAction.INITIALIZE_ORGANISME_STEPS,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        # TODO : duplicate query — also done in OrganismePermissionService.can_execute()
        # (Organisme existence check), dedupe when refactoring to ADR-009
        organisme = self.organisme_recruteur_repository.get_by_id(command.organisme_id)
        with transaction.atomic():
            organisme.initialiser_etapes()
            self.organisme_recruteur_repository.save(organisme)
            self.audit_log_writer.log_action(
                utilisateur_id=command.utilisateur.entity_id,
                entity=organisme,
                ressource_kind="OrganismeRecruteur",
                event_name="OrganismeEtapesInitialises",
            )
        return organisme
