from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel


def authorized_actions_of(
    organisme_role: AgentOrganismeRole,
    recrutement_role: AgentRecrutementRole | None,
) -> list[str]:
    return [
        action.value
        for action in OrganismePermissionService().authorized_actions_recrutement(
            organisme_role, recrutement_role=recrutement_role
        )
    ]


def set_authorized_actions(recrutement: RecrutementModel) -> None:
    recrutement_role = recrutement.recrutement_role  # type: ignore[attr-defined]
    recrutement.authorized_actions = authorized_actions_of(  # type: ignore[attr-defined]
        AgentOrganismeRole(recrutement.organisme_role),  # type: ignore[attr-defined]
        AgentRecrutementRole(recrutement_role) if recrutement_role else None,
    )
