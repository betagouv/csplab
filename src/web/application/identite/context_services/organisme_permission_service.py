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
from infrastructure.django_apps.users.models import UserModel

# Actions sans organisme existant : seul le statut staff autorise l'opération
_ACTIONS_SANS_ORGANISME: frozenset[OrganismeAction] = frozenset(
    {
        OrganismeAction.CREER_ORGANISME,
        OrganismeAction.LISTER_ORGANISMES,
    }
)

# Actions sur un organisme existant réservées au staff, hors rôles d'organisme
_ACTIONS_STAFF_AVEC_ORGANISME: frozenset[OrganismeAction] = frozenset(
    {OrganismeAction.MODIFIER_ORGANISME}
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
    OrganismeAction.GET_CANDIDATURE_DETAIL: frozenset(
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
    OrganismeAction.SET_RECRUTEMENTS_RESPONSABLE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    OrganismeAction.GET_MOTIFS_REFUS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.LIST_NOTES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.CREATE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.UPDATE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.DELETE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.LIST_DOCUMENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.READ_DOCUMENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.LIST_CONVERSATIONS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.READ_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.CREATE_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    OrganismeAction.REPLY_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
}

# -------------------------------------
# Authorisations niveau Recrutement
# -------------------------------------
# Actions pour lesquelles un MEMBRE n'a besoin d'aucun rôle sur le recrutement
_SANS_ROLE_RECRUTEMENT_REQUIS: frozenset[OrganismeAction] = frozenset(
    {OrganismeAction.LISTER_MES_RECRUTEMENTS, OrganismeAction.GET_MOTIFS_REFUS}
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
    OrganismeAction.GET_CANDIDATURE_DETAIL: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES: frozenset(
        {AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR}
    ),
    OrganismeAction.READ_DOCUMENT: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.LIST_DOCUMENTS: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.LIST_NOTES: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.CREATE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.UPDATE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.DELETE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.LIST_CONVERSATIONS: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.READ_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.CREATE_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    OrganismeAction.REPLY_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
}


def _agent_id(utilisateur: UserModel | Utilisateur) -> UUID:
    if isinstance(utilisateur, UserModel):
        return utilisateur.username
    return utilisateur.entity_id


class OrganismePermissionService:
    def can_execute(
        self,
        *,
        action: OrganismeAction,
        utilisateur: UserModel | Utilisateur,
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

        if utilisateur.is_staff and action in _ACTIONS_STAFF_AVEC_ORGANISME:
            return None

        if action not in _ROLES_REQUIS:
            raise OperationOrganismeRefusee()

        # Le staff agit en superviseur : lister_mes_recrutements lève le filtre agent
        if (
            utilisateur.is_staff
            and organisme_id
            and AgentOrganismeRole.SUPERVISEUR in _ROLES_REQUIS[action]
        ):
            return AgentOrganismeRole.SUPERVISEUR

        # TODO : duplicate query — agent-attach/update/revoke usecases run
        # near-identical OrganismeAgentModel lookups for the *target* agent right next
        # to this call (application/recruteur/usecases/{attach,update,revoke}
        # _organisme_agent.py); dedupe when refactoring to ADR-009
        agent_id = _agent_id(utilisateur)
        liaison = OrganismeAgentModel.objects.by_organisme_and_agent(
            organisme_id, agent_id
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
                    recrutement_id, agent_id
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
