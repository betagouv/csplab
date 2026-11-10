from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    set_authorized_actions,
)
from domain.identite.errors.organisme_permission_errors import OperationOrganismeRefusee
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


def get_recrutement(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> RecrutementModel:
    role = OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    if role is None:
        raise OperationOrganismeRefusee()
    try:
        recrutement = (
            RecrutementModel.objects.active_by_id(recrutement_id)
            .filter(organisme_id=organisme_id)
            .with_detail()
            .with_role_of(utilisateur.username)
            .with_organisme_role(role)
            .get()
        )
    except RecrutementModel.DoesNotExist as error:
        raise RecrutementInexistant(recrutement_id) from error
    set_authorized_actions(recrutement)
    return recrutement
