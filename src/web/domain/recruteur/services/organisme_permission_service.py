from uuid import UUID

from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole

_ROLES_REQUIS: dict[OrganismeAction, frozenset[AgentOrganismeRole]] = {
    OrganismeAction.GET_ORGANISME: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.INITIALIZE_ORGANISME_STEPS: frozenset(
        {AgentOrganismeRole.RESPONSABLE}
    ),
    OrganismeAction.UPDATE_ORGANISME_STEPS: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.LISTER_MES_RECRUTEMENTS: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
}

# Actions pour lesquelles le statut staff dispense d'un rôle réel sur l'organisme
_AUTORISE_POUR_STAFF: frozenset[OrganismeAction] = frozenset(
    {
        OrganismeAction.GET_ORGANISME,
        OrganismeAction.INITIALIZE_ORGANISME_STEPS,
        OrganismeAction.UPDATE_ORGANISME_STEPS,
    }
)


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
    ) -> AgentOrganismeRole | None:
        if est_staff and action in _AUTORISE_POUR_STAFF:
            return None
        roles_requis = _ROLES_REQUIS[action]
        role = self._organisme_agent_repository.get_role(
            organisme_id=organisme_id, agent_id=agent_id
        )
        if role not in roles_requis:
            raise AccesOrganismeRefuse(organisme_id)
        return role
