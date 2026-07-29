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
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)

# Actions pour lesquelles le statut staff dispense d'un rôle réel sur l'organisme
_AUTORISE_POUR_STAFF: frozenset[OrganismeAction] = frozenset(
    {
        OrganismeAction.GET_ORGANISME,
        OrganismeAction.INITIALIZE_ORGANISME_STEPS,
        OrganismeAction.UPDATE_ORGANISME_STEPS,
    }
)

# -------------------------------------
# Authorisations niveau Organisme
# -------------------------------------
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
    OrganismeAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
}

# -------------------------------------
# Authorisations niveau Recrutement
# -------------------------------------
# Actions pour lesquelles un MEMBRE n'a besoin d'aucun rôle sur le recrutement
_SANS_ROLE_RECRUTEMENT_REQUIS: frozenset[OrganismeAction] = frozenset(
    {OrganismeAction.LISTER_MES_RECRUTEMENTS}
)

# Actions pour lesquelles un MEMBRE doit avoir un rôle sur le recrutement
_ROLES_RECRUTEMENT_REQUIS: dict[OrganismeAction, frozenset[AgentRecrutementRole]] = {
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
}


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

        if (
            role == AgentOrganismeRole.MEMBRE
            and action not in _SANS_ROLE_RECRUTEMENT_REQUIS
        ):
            if recrutement_id is None:
                raise AccesRecrutementInconnu()

            recrutement_role = self._recrutement_agent_repository.get_role(
                recrutement_id=recrutement_id, agent_id=agent_id
            )
            if recrutement_role not in _ROLES_RECRUTEMENT_REQUIS[action]:
                raise AccesRecrutementRefuse(recrutement_id)

        return role
