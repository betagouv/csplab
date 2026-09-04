from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ddd.entity import Entity
from ddd.usecase_interface import IUsecase

from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_agent_query_service_interface import (
    IOrganismeAgentQueryService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.repositories.agent_repository_interface import IAgentRepository
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole


@dataclass
class AttachOrganismeAgentCommand:
    organisme_id: UUID
    agent_id: UUID
    role: AgentOrganismeRole
    utilisateur: Utilisateur


class AttachOrganismeAgentUsecase(
    IUsecase[AttachOrganismeAgentCommand, AgentOrganismeReadModel]
):
    def __init__(
        self,
        organisme_agent_repository: IOrganismeAgentRepository,
        organisme_agent_query_service: IOrganismeAgentQueryService,
        agent_repository: IAgentRepository,
        organisme_permission_service: OrganismePermissionService,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_agent_repository = organisme_agent_repository
        self.organisme_agent_query_service = organisme_agent_query_service
        self.agent_repository = agent_repository
        self.organisme_permission_service = organisme_permission_service
        self.audit_log_writer = audit_log_writer

    def execute(self, command: AttachOrganismeAgentCommand) -> AgentOrganismeReadModel:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.ATTACH_ORGANISME_AGENT,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        if not self.agent_repository.exists(command.agent_id):
            raise ProfilAgentNexistePas(command.agent_id)

        agent_is_revoked = self.organisme_agent_repository.is_revoked(
            organisme_id=command.organisme_id, agent_id=command.agent_id
        )
        if agent_is_revoked:
            self.organisme_agent_repository.reattach(
                organisme_id=command.organisme_id,
                agent_id=command.agent_id,
                role=command.role,
            )
        else:
            self.organisme_agent_repository.attach(
                organisme_id=command.organisme_id,
                agent_id=command.agent_id,
                role=command.role,
            )
        self.audit_log_writer.log_action(
            utilisateur_id=command.utilisateur.entity_id,
            entity=Entity(entity_id=command.agent_id),
            ressource_kind="AgentOrganisme",
            event_name="AgentOrganismeRoleAttache",
        )
        agent_organisme = self.organisme_agent_query_service.get_one(
            organisme_id=command.organisme_id, agent_id=command.agent_id
        )
        return cast(AgentOrganismeReadModel, agent_organisme)
