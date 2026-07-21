from uuid import UUID

from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole

_ROLES_REQUIS: dict[OrganismeAction, AgentOrganismeRole] = {
    OrganismeAction.GET_ORGANISME: AgentOrganismeRole.RESPONSABLE,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS: AgentOrganismeRole.RESPONSABLE,
    OrganismeAction.UPDATE_ORGANISME_STEPS: AgentOrganismeRole.RESPONSABLE,
    OrganismeAction.LISTER_MES_RECRUTEMENTS: AgentOrganismeRole.RESPONSABLE,
}


class OrganismePermissionService:
    def __init__(self, organisme_agent_repository: IOrganismeAgentRepository) -> None:
        self._organisme_agent_repository = organisme_agent_repository

    def est_autorise(
        self,
        *,
        action: OrganismeAction,
        organisme_id: UUID,
        agent_id: UUID,
        est_staff: bool,
    ) -> None:
        role_requis = _ROLES_REQUIS[action]
        if est_staff:
            return
        role = self._organisme_agent_repository.get_role(
            organisme_id=organisme_id, agent_id=agent_id
        )
        if role != role_requis:
            raise AccesOrganismeRefuse(organisme_id)
