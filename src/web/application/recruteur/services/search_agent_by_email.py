from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.users.models import ProfilAgentModel, UserModel


def search_agent_by_email(
    *, organisme_id: UUID, utilisateur: UserModel, email: str
) -> ProfilAgentModel | None:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.SEARCH_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    return ProfilAgentModel.objects.par_email(email).first()
