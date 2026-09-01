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
    ):
        self.organisme_agent_repository = organisme_agent_repository
        self.organisme_agent_query_service = organisme_agent_query_service
        self.agent_repository = agent_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: AttachOrganismeAgentCommand) -> AgentOrganismeReadModel:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.ATTACH_ORGANISME_AGENT,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        if not self.agent_repository.exists(command.agent_id):
            # TODO: create agent if not exists
            pass

        self.organisme_agent_repository.attach(
            organisme_id=command.organisme_id,
            agent_id=command.agent_id,
            role=command.role,
        )
        agent_organisme = self.organisme_agent_query_service.get_one(
            organisme_id=command.organisme_id, agent_id=command.agent_id
        )
        return cast(AgentOrganismeReadModel, agent_organisme)
