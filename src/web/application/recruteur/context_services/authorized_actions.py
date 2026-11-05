from collections.abc import Collection
from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel

_permissions = OrganismePermissionService()


def authorized_actions_of(
    organisme_role: AgentOrganismeRole,
    recrutement_role: AgentRecrutementRole | None,
) -> list[str]:
    return [
        action.value
        for action in _permissions.authorized_actions_recrutement(
            organisme_role, recrutement_role=recrutement_role
        )
    ]


def authorized_actions_of_organisme(
    role: AgentOrganismeRole,
    organisme_id: UUID,
    *,
    utilisateur: UserModel,
    organisme_ids_responsable: Collection[UUID],
) -> list[str]:
    actions = {
        *_permissions.authorized_actions_organisme(
            role,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
            organisme_ids_responsable=organisme_ids_responsable,
        ),
        *_permissions.authorized_actions_staff_organisme(utilisateur),
    }
    return [action.value for action in OrganismeAction if action in actions]


def set_authorized_actions(recrutement: RecrutementModel) -> None:
    recrutement_role = recrutement.recrutement_role  # type: ignore[attr-defined]
    recrutement.authorized_actions = authorized_actions_of(  # type: ignore[attr-defined]
        AgentOrganismeRole(recrutement.organisme_role),  # type: ignore[attr-defined]
        AgentRecrutementRole(recrutement_role) if recrutement_role else None,
    )
