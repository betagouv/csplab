from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.get_recrutement_etapes import (
    recrutement_etapes,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.messagerie.models import unread_conversations_count
from infrastructure.django_apps.recruteur.models.etape import EtapeModel
from infrastructure.django_apps.users.models import UserModel


def list_candidatures_et_etapes(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> tuple[QuerySet[CandidatureModel], list[EtapeModel]]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    etapes = recrutement_etapes(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    candidatures = CandidatureModel.objects.by_recrutement(recrutement_id).annotate(
        unread_conversations=unread_conversations_count(utilisateur.username)
    )
    return candidatures, etapes
