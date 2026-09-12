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
    OrganismeAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES: frozenset(
        {AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE}
    ),
    OrganismeAction.LIST_ORGANISME_AGENTS: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.SEARCH_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.ATTACH_ORGANISME_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.UPDATE_ORGANISME_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.REVOKE_ORGANISME_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.CREATE_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.LIST_RECRUTEMENT_AGENTS: frozenset(
        {AgentOrganismeRole.RESPONSABLE}
    ),
    OrganismeAction.ADD_RECRUTEMENT_AGENT: frozenset({AgentOrganismeRole.RESPONSABLE}),
    OrganismeAction.UPDATE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.RESPONSABLE}
    ),
    OrganismeAction.REVOKE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.RESPONSABLE}
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


def can_execute(
    *,
    action: OrganismeAction,
    utilisateur: Utilisateur,
    organisme_id: UUID | None = None,
    recrutement_id: UUID | None = None,
) -> AgentOrganismeRole | None:
    if utilisateur.is_staff and action in _ACTIONS_SANS_ORGANISME:
        return None

    if organisme_id and not OrganismeModel.objects.filter(id=organisme_id).exists():
        raise OrganismeNexistePas(str(organisme_id))

    if utilisateur.is_staff and action in _AUTORISE_POUR_STAFF:
        return None

    if action not in _ROLES_REQUIS:
        raise OperationOrganismeRefusee()

    roles_requis = _ROLES_REQUIS[action]
    role_value = (
        OrganismeAgentModel.objects.active()
        .filter(organisme_id=organisme_id, agent_id=utilisateur.entity_id)
        .values_list("role", flat=True)
        .first()
    )
    role = AgentOrganismeRole(role_value) if role_value is not None else None
    if role not in roles_requis:
        raise AccesOrganismeRefuse(cast(UUID, organisme_id))

    membre_doit_avoir_role_recrutement = (
        role == AgentOrganismeRole.MEMBRE
        and action not in _SANS_ROLE_RECRUTEMENT_REQUIS
    )
    if membre_doit_avoir_role_recrutement:
        if recrutement_id is None:
            raise AccesRecrutementInconnu()
        recrutement_role_value = (
            RecrutementAgentModel.objects.active()
            .filter(recrutement_id=recrutement_id, agent_id=utilisateur.entity_id)
            .values_list("role", flat=True)
            .first()
        )
        recrutement_role = (
            AgentRecrutementRole(recrutement_role_value)
            if recrutement_role_value is not None
            else None
        )
        if recrutement_role not in _ROLES_RECRUTEMENT_REQUIS[action]:
            raise AccesRecrutementRefuse(recrutement_id)

    return role
