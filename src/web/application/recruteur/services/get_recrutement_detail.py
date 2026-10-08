from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


def get_recrutement_detail(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> RecrutementModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    try:
        return (
            RecrutementModel.objects.active_by_id(recrutement_id)
            .filter(organisme_id=organisme_id)
            .with_detail()
            .with_role_of(utilisateur.username)
            .get()
        )
    except RecrutementModel.DoesNotExist as error:
        raise RecrutementInexistant(recrutement_id) from error
