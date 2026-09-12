from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.users.models import ProfilAgentModel


def search_agent_by_email(
    *, organisme_id: UUID, utilisateur: Utilisateur, email: str
) -> ProfilAgentModel | None:
    can_execute(
        action=OrganismeAction.SEARCH_AGENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )

    return ProfilAgentModel.objects.par_email(email).first()
