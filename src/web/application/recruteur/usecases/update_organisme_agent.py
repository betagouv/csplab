from dataclasses import dataclass
from typing import cast
from uuid import UUID

from ddd.usecase_interface import IUsecase

from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_agent_query_service_interface import (
    IOrganismeAgentQueryService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole


@dataclass
class UpdateOrganismeAgentCommand:
    organisme_id: UUID
    agent_id: UUID
    role: AgentOrganismeRole
    utilisateur: Utilisateur


class UpdateOrganismeAgentUsecase(
    IUsecase[UpdateOrganismeAgentCommand, AgentOrganismeReadModel]
):
    def __init__(
        self,
        organisme_agent_repository: IOrganismeAgentRepository,
        organisme_agent_query_service: IOrganismeAgentQueryService,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_agent_repository = organisme_agent_repository
        self.organisme_agent_query_service = organisme_agent_query_service
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: UpdateOrganismeAgentCommand) -> AgentOrganismeReadModel:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.UPDATE_ORGANISME_AGENT,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        self.organisme_agent_repository.update_role(
            organisme_id=command.organisme_id,
            agent_id=command.agent_id,
            role=command.role,
        )
        agent_organisme = self.organisme_agent_query_service.get_one(
            organisme_id=command.organisme_id, agent_id=command.agent_id
        )
        return cast(AgentOrganismeReadModel, agent_organisme)
