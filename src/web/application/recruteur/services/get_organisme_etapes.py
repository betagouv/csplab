from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def get_organisme_etapes(
    *, organisme_id: UUID, utilisateur: UserModel
) -> OrganismeModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_ORGANISME,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
    )
    try:
        return OrganismeModel.objects.etapes_of(organisme_id).get()
    except OrganismeModel.DoesNotExist as error:
        raise OrganismeNexistePas(str(organisme_id)) from error
