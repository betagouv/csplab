from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)
from application.recruteur.services.organisme_agent_query_service_interface import (
    IOrganismeAgentQueryService,
)
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
    ):
        self.organisme_agent_query_service = organisme_agent_query_service

    def execute(
        self, command: ListOrganismeAgentsQuery
    ) -> list[AgentOrganismeReadModel]:
        can_execute(
            action=OrganismeAction.LIST_ORGANISME_AGENTS,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        return self.organisme_agent_query_service.list_by_organisme(
            organisme_id=command.organisme_id
        )
