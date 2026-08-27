from typing import cast
from uuid import UUID

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_agent_repository_interface import (
    IRecrutementAgentRepository,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)

# Actions sans organisme existant : seul le statut staff autorise l'opération
_ACTIONS_SANS_ORGANISME: frozenset[OrganismeAction] = frozenset(
    {
        OrganismeAction.CREER_ORGANISME,
        OrganismeAction.LISTER_ORGANISMES,
    }
)

# Actions pour lesquelles le statut staff dispense d'un rôle réel sur l'organisme
_AUTORISE_POUR_STAFF: frozenset[OrganismeAction] = frozenset(
    {
        OrganismeAction.GET_ORGANISME,
        OrganismeAction.INITIALIZE_ORGANISME_STEPS,
        OrganismeAction.UPDATE_ORGANISME_STEPS,
        OrganismeAction.CREER_ORGANISME,
        OrganismeAction.LISTER_ORGANISMES,
        OrganismeAction.MODIFIER_ORGANISME,
    }
)

# -------------------------------------
# Authorisations niveau Organisme
# -------------------------------------
_ROLES_REQUIS: dict[OrganismeAction, frozenset[AgentOrganismeRole]] = {
    OrganismeAction.GET_ORGANISME: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.INITIALIZE_ORGANISME_STEPS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    OrganismeAction.UPDATE_ORGANISME_STEPS: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.LISTER_MES_RECRUTEMENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.MEMBRE}
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
    OrganismeAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES: frozenset(
        {AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR}
    ),
}


class OrganismePermissionService:
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        organisme_agent_repository: IOrganismeAgentRepository,
        recrutement_agent_repository: IRecrutementAgentRepository,
    ) -> None:
        self._organisme_recruteur_repository = organisme_recruteur_repository
        self._organisme_agent_repository = organisme_agent_repository
        self._recrutement_agent_repository = recrutement_agent_repository

    def est_autorise(
        self,
        *,
        action: OrganismeAction,
        utilisateur: Utilisateur,
        organisme_id: UUID | None = None,
        recrutement_id: UUID | None = None,
    ) -> AgentOrganismeRole | None:
        if utilisateur.is_staff and action in _ACTIONS_SANS_ORGANISME:
            return None

        self._organisme_recruteur_repository.get_by_id(organisme_id)

        if utilisateur.is_staff and action in _AUTORISE_POUR_STAFF:
            return None

        if action not in _ROLES_REQUIS:
            raise OperationOrganismeRefusee()

        roles_requis = _ROLES_REQUIS[action]
        role = self._organisme_agent_repository.get_role(
            organisme_id=cast(UUID, organisme_id), agent_id=utilisateur.entity_id
        )
        if role not in roles_requis:
            raise AccesOrganismeRefuse(cast(UUID, organisme_id))

        if (
            role == AgentOrganismeRole.MEMBRE
            and action not in _SANS_ROLE_RECRUTEMENT_REQUIS
        ):
            if recrutement_id is None:
                raise AccesRecrutementInconnu()

            recrutement_role = self._recrutement_agent_repository.get_role(
                recrutement_id=recrutement_id, agent_id=utilisateur.entity_id
            )
            if recrutement_role not in _ROLES_RECRUTEMENT_REQUIS[action]:
                raise AccesRecrutementRefuse(recrutement_id)

        return role
