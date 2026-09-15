from typing import cast
from uuid import UUID

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.organisme import (
    OrganismeAgentModel,
    OrganismeModel,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
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
        OrganismeAction.LIST_ORGANISME_AGENTS,
        OrganismeAction.SEARCH_AGENT,
        OrganismeAction.ATTACH_ORGANISME_AGENT,
        OrganismeAction.UPDATE_ORGANISME_AGENT,
        OrganismeAction.REVOKE_ORGANISME_AGENT,
        OrganismeAction.CREATE_AGENT,
        OrganismeAction.LIST_RECRUTEMENT_AGENTS,
        OrganismeAction.ADD_RECRUTEMENT_AGENT,
        OrganismeAction.UPDATE_RECRUTEMENT_AGENT,
        OrganismeAction.REVOKE_RECRUTEMENT_AGENT,
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
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.LIST_ORGANISME_AGENTS: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.SEARCH_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.ATTACH_ORGANISME_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.UPDATE_ORGANISME_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.REVOKE_ORGANISME_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.CREATE_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.LIST_RECRUTEMENT_AGENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    OrganismeAction.ADD_RECRUTEMENT_AGENT: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    OrganismeAction.UPDATE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    OrganismeAction.REVOKE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
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
    def can_execute(
        self,
        *,
        action: OrganismeAction,
        utilisateur: Utilisateur,
        organisme_id: UUID | None = None,
        recrutement_id: UUID | None = None,
    ) -> AgentOrganismeRole | None:
        if utilisateur.is_staff and action in _ACTIONS_SANS_ORGANISME:
            return None

        # TODO : duplicate query — callers passing organisme_id typically also fetch the
        # full Organisme/OrganismeRecruteur row via their repository right around this
        # call (application/*/usecases/*.py); dedupe when refactoring to ADR-009
        if organisme_id and not OrganismeModel.objects.filter(id=organisme_id).exists():
            raise OrganismeNexistePas(str(organisme_id))

        if utilisateur.is_staff and action in _AUTORISE_POUR_STAFF:
            return None

        if action not in _ROLES_REQUIS:
            raise OperationOrganismeRefusee()

        # TODO : duplicate query — agent-attach/update/revoke usecases run
        # near-identical OrganismeAgentModel lookups for the *target* agent right next
        # to this call (application/recruteur/usecases/{attach,update,revoke}
        # _organisme_agent.py); dedupe when refactoring to ADR-009
        liaison = OrganismeAgentModel.objects.filter(
            organisme_id=organisme_id, agent_id=utilisateur.entity_id
        ).first()
        role = AgentOrganismeRole(liaison.role) if liaison else None
        if role not in _ROLES_REQUIS[action]:
            raise AccesOrganismeRefuse(cast(UUID, organisme_id))

        if (
            role == AgentOrganismeRole.AGENT
            and action not in _SANS_ROLE_RECRUTEMENT_REQUIS
        ):
            if recrutement_id is None:
                raise AccesRecrutementInconnu()

            # TODO : duplicate query — overlaps the
            # recrutement_repository.get_by_id(...) call usecases already made just
            # above (application/recruteur/usecases/{get,init,update}
            # _recrutement_etapes.py); dedupe when refactoring to ADR-009
            recrutement_liaison = (
                RecrutementAgentModel.objects.by_recrutement_and_agent(
                    recrutement_id, utilisateur.entity_id
                ).first()
            )
            recrutement_role = (
                AgentRecrutementRole(recrutement_liaison.role)
                if recrutement_liaison
                else None
            )
            if recrutement_role not in _ROLES_RECRUTEMENT_REQUIS[action]:
                raise AccesRecrutementRefuse(recrutement_id)

        return role
