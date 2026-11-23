from uuid import UUID

from application.identite.context_services.permission_service import (
    PermissionService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel


def search_agent_by_email(
    *, organisme_id: UUID, utilisateur: UserModel, email: str
) -> ProfilAgentModel | None:
    PermissionService().can_execute(
        action=PermissionAction.SEARCH_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    return ProfilAgentModel.objects.par_email(email).first()
