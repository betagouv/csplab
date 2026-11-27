from collections.abc import Collection
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
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_agent_errors import (
    MembreRecrutementNonModifiable,
    RoleRecrutementNonAutorise,
)
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
_ACTIONS_SANS_ORGANISME: frozenset[PermissionAction] = frozenset(
    {
        PermissionAction.CREATE_ORGANISME,
        PermissionAction.LIST_ORGANISMES,
    }
)

# Actions sur un organisme existant réservées au staff, hors rôles d'organisme
_ACTIONS_STAFF_AVEC_ORGANISME: frozenset[PermissionAction] = frozenset(
    {PermissionAction.UPDATE_ORGANISME}
)

# -------------------------------------
# Authorisations niveau Organisme
# -------------------------------------
_ROLES_REQUIS: dict[PermissionAction, frozenset[AgentOrganismeRole]] = {
    PermissionAction.GET_ORGANISME: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    PermissionAction.INITIALIZE_ORGANISME_STEPS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.UPDATE_ORGANISME_STEPS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.LIST_RECRUTEMENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.GET_RECRUTEMENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.GET_CANDIDATURE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.CHANGE_ETAPE_CANDIDATURES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_ORGANISME_AGENTS: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    PermissionAction.SEARCH_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.ATTACH_ORGANISME_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.UPDATE_ORGANISME_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.REVOKE_ORGANISME_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.CREATE_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_RECRUTEMENT_AGENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.ADD_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.UPDATE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.REVOKE_RECRUTEMENT_AGENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.SET_RECRUTEMENTS_RESPONSABLE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.GET_MOTIFS_REFUS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_NOTES: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.CREATE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.UPDATE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.DELETE_NOTE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_DOCUMENTS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.READ_DOCUMENT: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_CONVERSATIONS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.READ_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.CREATE_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.REPLY_CONVERSATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.LIST_TAGS: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.CREATE_TAG: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    PermissionAction.UPDATE_TAG: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    PermissionAction.DELETE_TAG: frozenset({AgentOrganismeRole.SUPERVISEUR}),
    PermissionAction.MANAGE_TAG_ON_APPLICATION: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
    PermissionAction.GRANT_RECRUTEMENT_RESPONSABLE: frozenset(
        {AgentOrganismeRole.SUPERVISEUR}
    ),
    PermissionAction.MANAGE_TAG_ON_MEMBER: frozenset(
        {AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT}
    ),
}

_ROLES_ATTRIBUABLES_PAR_NON_SUPERVISEUR: frozenset[str] = frozenset(
    {AgentRecrutementRole.RECRUTEUR.value, AgentRecrutementRole.CONTRIBUTEUR.value}
)

# -------------------------------------
# Authorisations niveau Recrutement
# -------------------------------------
# Actions pour lesquelles un MEMBRE n'a besoin d'aucun rôle sur le recrutement
_SANS_ROLE_RECRUTEMENT_REQUIS: frozenset[PermissionAction] = frozenset(
    {
        PermissionAction.LIST_RECRUTEMENTS,
        PermissionAction.GET_MOTIFS_REFUS,
        PermissionAction.LIST_TAGS,
    }
)

# Actions sans recrutement ciblé : un MEMBRE doit être RESPONSABLE d'au moins un
# recrutement de l'organisme
_RESPONSABLE_D_UN_RECRUTEMENT_REQUIS: frozenset[PermissionAction] = frozenset(
    {PermissionAction.SEARCH_AGENT, PermissionAction.CREATE_AGENT}
)

# Actions pour lesquelles un MEMBRE doit avoir un rôle sur le recrutement
_ROLES_RECRUTEMENT_REQUIS: dict[PermissionAction, frozenset[AgentRecrutementRole]] = {
    PermissionAction.GET_RECRUTEMENT: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.GET_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.UPDATE_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.INIT_RECRUTEMENT_ETAPES: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.GET_CANDIDATURE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.CHANGE_ETAPE_CANDIDATURES: frozenset(
        {AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR}
    ),
    PermissionAction.LIST_RECRUTEMENT_AGENTS: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.ADD_RECRUTEMENT_AGENT: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.UPDATE_RECRUTEMENT_AGENT: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.REVOKE_RECRUTEMENT_AGENT: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
    PermissionAction.READ_DOCUMENT: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.LIST_DOCUMENTS: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.LIST_NOTES: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.CREATE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.UPDATE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.DELETE_NOTE: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.LIST_CONVERSATIONS: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.READ_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.CREATE_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.REPLY_CONVERSATION: frozenset(
        {
            AgentRecrutementRole.RESPONSABLE,
            AgentRecrutementRole.RECRUTEUR,
            AgentRecrutementRole.CONTRIBUTEUR,
        }
    ),
    PermissionAction.MANAGE_TAG_ON_APPLICATION: frozenset(
        {AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR}
    ),
    PermissionAction.GRANT_RECRUTEMENT_RESPONSABLE: frozenset(),
    PermissionAction.MANAGE_TAG_ON_MEMBER: frozenset(
        {AgentRecrutementRole.RESPONSABLE}
    ),
}

_ACTIONS_SUR_MEMBRE_RECRUTEMENT: frozenset[PermissionAction] = frozenset(
    {
        PermissionAction.UPDATE_RECRUTEMENT_AGENT,
        PermissionAction.REVOKE_RECRUTEMENT_AGENT,
    }
)

# Actions ciblant un recrutement précis : hors périmètre des actions exposées au
# niveau de l'utilisateur et de l'organisme
_ACTIONS_NIVEAU_RECRUTEMENT: frozenset[PermissionAction] = frozenset(
    _ROLES_RECRUTEMENT_REQUIS
)


def _ordonnees(actions: frozenset[PermissionAction]) -> list[PermissionAction]:
    return [action for action in PermissionAction if action in actions]


def _agent_id(utilisateur: UserModel | Utilisateur) -> UUID:
    if isinstance(utilisateur, UserModel):
        return utilisateur.username
    return utilisateur.entity_id


class PermissionService:
    def _can_manage_member(
        self,
        *,
        demandeur_role: AgentOrganismeRole | None,
        demandeur_id: UUID,
        member: RecrutementAgentModel,
    ) -> bool:
        return (
            demandeur_role
            in _ROLES_REQUIS[PermissionAction.GRANT_RECRUTEMENT_RESPONSABLE]
            or member.role != AgentRecrutementRole.RESPONSABLE.value
            or member.agent_id == demandeur_id
        )

    def check_member_manageable(
        self,
        *,
        demandeur_role: AgentOrganismeRole | None,
        demandeur_id: UUID,
        member: RecrutementAgentModel,
    ) -> None:
        if not self._can_manage_member(
            demandeur_role=demandeur_role, demandeur_id=demandeur_id, member=member
        ):
            raise MembreRecrutementNonModifiable(member.role)

    def check_role_grantable(
        self, *, demandeur_role: AgentOrganismeRole | None, role: str
    ) -> None:
        if (
            demandeur_role
            not in _ROLES_REQUIS[PermissionAction.GRANT_RECRUTEMENT_RESPONSABLE]
            and role not in _ROLES_ATTRIBUABLES_PAR_NON_SUPERVISEUR
        ):
            raise RoleRecrutementNonAutorise(role)

    def authorize(
        self,
        *,
        action: PermissionAction,
        utilisateur: UserModel | Utilisateur,
        organisme_id: UUID | None = None,
        recrutement_id: UUID | None = None,
    ) -> AgentOrganismeRole | None:
        if utilisateur.is_staff and action in _ACTIONS_SANS_ORGANISME:
            return None

        # TODO : duplicate query — callers passing organisme_id typically also fetch the
        # full Organisme/OrganismeRecruteur row via their repository right around this
        # call (application/*/usecases/*.py); dedupe when refactoring to ADR-009
        if organisme_id and not OrganismeModel.objects.by_id(organisme_id).exists():
            raise OrganismeNexistePas(str(organisme_id))

        if utilisateur.is_staff and action in _ACTIONS_STAFF_AVEC_ORGANISME:
            return None

        if action not in _ROLES_REQUIS:
            raise OperationOrganismeRefusee()

        # Le staff agit en superviseur : list_recrutements lève le filtre agent
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
            and action in _RESPONSABLE_D_UN_RECRUTEMENT_REQUIS
        ):
            if not RecrutementAgentModel.objects.is_responsable_dans_organisme(
                agent_id, cast(UUID, organisme_id)
            ):
                raise AccesOrganismeRefuse(cast(UUID, organisme_id))
        elif (
            role == AgentOrganismeRole.AGENT
            and action not in _SANS_ROLE_RECRUTEMENT_REQUIS
        ):
            if recrutement_id is None:
                raise AccesRecrutementInconnu()

            # TODO : duplicate query — overlaps the
            # recrutement_repository.get_by_id(...) call usecases already made just
            # above (application/recruteur/usecases/{init,update}
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
            if recrutement_role not in _ROLES_RECRUTEMENT_REQUIS.get(
                action, frozenset()
            ):
                raise AccesRecrutementRefuse(recrutement_id)

        return role

    def authorized_actions_user(self, utilisateur: UserModel) -> list[PermissionAction]:
        if not utilisateur.is_staff:
            return []
        return _ordonnees(_ACTIONS_SANS_ORGANISME | _ACTIONS_STAFF_AVEC_ORGANISME)

    def authorized_actions_staff_organisme(
        self, utilisateur: UserModel
    ) -> list[PermissionAction]:
        if not utilisateur.is_staff:
            return []
        return _ordonnees(_ACTIONS_STAFF_AVEC_ORGANISME)

    def authorized_actions_organisme(
        self,
        role: AgentOrganismeRole,
        *,
        utilisateur: UserModel,
        organisme_id: UUID,
        organisme_ids_responsable: Collection[UUID],
    ) -> list[PermissionAction]:
        if utilisateur.is_staff:
            role = AgentOrganismeRole.SUPERVISEUR
        exclues = _ACTIONS_NIVEAU_RECRUTEMENT
        if (
            role == AgentOrganismeRole.AGENT
            and organisme_id not in organisme_ids_responsable
        ):
            exclues |= _RESPONSABLE_D_UN_RECRUTEMENT_REQUIS
        return _ordonnees(
            frozenset(
                action
                for action, roles_requis in _ROLES_REQUIS.items()
                if role in roles_requis
            )
            - exclues
        )

    def authorized_actions_recrutement(
        self,
        role: AgentOrganismeRole,
        *,
        recrutement_role: AgentRecrutementRole | None,
    ) -> list[PermissionAction]:
        return _ordonnees(
            frozenset(
                action
                for action in _ACTIONS_NIVEAU_RECRUTEMENT
                if role in _ROLES_REQUIS[action]
                and (
                    role == AgentOrganismeRole.SUPERVISEUR
                    or recrutement_role in _ROLES_RECRUTEMENT_REQUIS[action]
                )
            )
        )

    def authorized_actions_member(
        self,
        *,
        demandeur_role: AgentOrganismeRole | None,
        demandeur_id: UUID,
        member: RecrutementAgentModel,
    ) -> list[PermissionAction]:
        if not self._can_manage_member(
            demandeur_role=demandeur_role, demandeur_id=demandeur_id, member=member
        ):
            return []
        return _ordonnees(_ACTIONS_SUR_MEMBRE_RECRUTEMENT)
