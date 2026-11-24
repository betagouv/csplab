from uuid import UUID

from application.identite.context_services.permission_service import (
    PermissionService,
)
from application.recruteur.context_services.authorized_actions import (
    set_etape_actions_of_recrutement,
)
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.recruteur.models.etape import (
    EtapeModel,
    etapes_ordonnees,
)
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


def recrutement_etapes(*, organisme_id: UUID, recrutement_id: UUID) -> list[EtapeModel]:
    try:
        recrutement = (
            RecrutementModel.objects.active_by_id(recrutement_id)
            .filter(organisme_id=organisme_id)
            .get()
        )
    except RecrutementModel.DoesNotExist as error:
        raise RecrutementInexistant(recrutement_id) from error
    return etapes_ordonnees(recrutement, recrutement.etapes.with_nb_candidatures())


def get_recrutement_etapes(
    *, organisme_id: UUID, recrutement_id: UUID, utilisateur: UserModel
) -> list[EtapeModel]:
    PermissionService().authorize(
        action=PermissionAction.GET_RECRUTEMENT_ETAPES,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    etapes = recrutement_etapes(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    set_etape_actions_of_recrutement(
        etapes,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        utilisateur=utilisateur,
    )
    return etapes
