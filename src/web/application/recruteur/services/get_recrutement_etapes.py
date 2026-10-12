from uuid import UUID

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


def get_recrutement_etapes(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> list[EtapeModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_RECRUTEMENT_ETAPES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    try:
        recrutement = (
            RecrutementModel.objects.active_by_id(recrutement_id)
            .filter(organisme_id=organisme_id)
            .get()
        )
    except RecrutementModel.DoesNotExist as error:
        raise RecrutementInexistant(recrutement_id) from error
    return etapes_ordonnees(recrutement)
