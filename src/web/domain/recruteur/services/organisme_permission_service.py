from uuid import UUID

from domain.recruteur.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
)
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.repositories.recrutement_agent_repository_interface import (
    IRecrutementAgentRepository,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole

# Actions pour lesquelles un AGENT doit avoir un rôle sur l'organisme
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

# Actions pour lesquelles un MEMBRE doit en plus être affecté au recrutement visé
_REQUIERT_ROLE_RECRUTEMENT: frozenset[OrganismeAction] = frozenset(
    {OrganismeAction.VOIR_DETAIL_RECRUTEMENT}
)


class OrganismePermissionService:
    def __init__(
        self,
        organisme_agent_repository: IOrganismeAgentRepository,
        recrutement_agent_repository: IRecrutementAgentRepository,
    ) -> None:
        self._organisme_agent_repository = organisme_agent_repository
        self._recrutement_agent_repository = recrutement_agent_repository

    def est_autorise(
        self,
        *,
        action: OrganismeAction,
        organisme_id: UUID,
        agent_id: UUID,
        est_staff: bool,
        recrutement_id: UUID | None = None,
    ) -> AgentOrganismeRole | None:
        if est_staff and action in _AUTORISE_POUR_STAFF:
            return None

        roles_requis = _ROLES_REQUIS[action]
        role = self._organisme_agent_repository.get_role(
            organisme_id=organisme_id, agent_id=agent_id
        )
        if role not in roles_requis:
            raise AccesOrganismeRefuse(organisme_id)

        if role == AgentOrganismeRole.MEMBRE and action in _REQUIERT_ROLE_RECRUTEMENT:
            if recrutement_id is None:
                raise AccesRecrutementInconnu()

            recrutement_role = self._recrutement_agent_repository.get_role(
                recrutement_id=recrutement_id, agent_id=agent_id
            )
            if recrutement_role is None:
                raise AccesRecrutementRefuse(recrutement_id)

        return role
