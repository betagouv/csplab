from dataclasses import dataclass
from uuid import UUID

from ddd.entity import Entity
from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_agent_query_service_interface import (
    IOrganismeAgentQueryService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class ListOrganismeAgentsQuery:
    organisme_id: UUID
    utilisateur: Utilisateur


class ListOrganismeAgentsUsecase(
    IUsecase[ListOrganismeAgentsQuery, list[AgentOrganismeReadModel]]
):
    def __init__(
        self,
        organisme_agent_query_service: IOrganismeAgentQueryService,
        organisme_permission_service: OrganismePermissionService,
        audit_log_writer: AuditLogWriter,
    ):
        self.organisme_agent_query_service = organisme_agent_query_service
        self.organisme_permission_service = organisme_permission_service
        self.audit_log_writer = audit_log_writer

    def execute(
        self, command: ListOrganismeAgentsQuery
    ) -> list[AgentOrganismeReadModel]:
        self.organisme_permission_service.can_execute(
            action=OrganismeAction.LIST_ORGANISME_AGENTS,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        agents = self.organisme_agent_query_service.list_by_organisme(
            organisme_id=command.organisme_id
        )
        self.audit_log_writer.log_action(
            utilisateur_id=command.utilisateur.entity_id,
            entity=Entity(entity_id=command.organisme_id),
            ressource_kind="OrganismeRecruteur",
            event_name="OrganismeAgentsConsultes",
        )
        return agents
