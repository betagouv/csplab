from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def get_organisme_etapes(
    *, organisme_id: UUID, utilisateur: UserModel
) -> OrganismeModel:
    # can_execute lève OrganismeNexistePas si l'organisme n'existe pas
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_ORGANISME,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    return OrganismeModel.objects.only("id", "etapes").get(id=organisme_id)
