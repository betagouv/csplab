from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.verse import Verse

from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class UpdateOrganismeCommand:
    organisme_id: UUID
    name: str | None
    verse: Verse | None
    managed_ats: bool | None
    utilisateur: Utilisateur


class UpdateOrganismeUsecase(IUsecase[UpdateOrganismeCommand, Organisme]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismePermissionService,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service
        self.audit_log_writer = audit_log_writer

    def can_execute(self, command: UpdateOrganismeCommand) -> Organisme:
        organisme = self.organisme_repository.get_by_id(command.organisme_id)
        self.permission_service.est_autorise(
            action=OrganismeAction.MODIFIER_ORGANISME,
            utilisateur=command.utilisateur,
        )
        return organisme

    def execute(self, command: UpdateOrganismeCommand) -> Organisme:
        organisme = self.can_execute(command)
        organisme.modifier(
            nom=command.name, versant=command.verse, gestion_ats=command.managed_ats
        )
        self.organisme_repository.save(organisme)
        self.audit_log_writer.drain_events(
            utilisateur_id=command.utilisateur.entity_id, aggregate=organisme
        )
        return organisme
