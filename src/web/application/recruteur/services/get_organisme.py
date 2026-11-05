from typing import cast
from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    authorized_actions_of_organisme,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.django_apps.users.models import UserModel


def get_organisme(*, organisme_id: UUID, utilisateur: UserModel) -> OrganismeModel:
    role = cast(
        AgentOrganismeRole,
        OrganismePermissionService().can_execute(
            action=OrganismeAction.GET_ORGANISME,
            utilisateur=utilisateur,
            organisme_id=organisme_id,
        ),
    )
    try:
        organisme = OrganismeModel.objects.by_id(organisme_id).get()
    except OrganismeModel.DoesNotExist as error:
        raise OrganismeNexistePas(str(organisme_id)) from error
    organisme.authorized_actions = authorized_actions_of_organisme(  # type: ignore[attr-defined]
        role, organisme.id, utilisateur=utilisateur
    )
    return organisme
