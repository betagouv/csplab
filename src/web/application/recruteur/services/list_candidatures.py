from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import RecrutementInexistant
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.messagerie.models import unread_conversations_count
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from infrastructure.django_apps.users.models import UserModel


def list_candidatures(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    utilisateur: UserModel,
) -> tuple[RecrutementModel, QuerySet[CandidatureModel]]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.GET_RECRUTEMENT,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    recrutement = (
        RecrutementModel.objects.active_by_id(recrutement_id)
        .filter(organisme_id=organisme_id)
        .with_list_version(utilisateur.username)
        .first()
    )
    if recrutement is None:
        raise RecrutementInexistant(recrutement_id)
    candidatures = CandidatureModel.objects.by_recrutement(recrutement_id).annotate(
        unread_conversations=unread_conversations_count(utilisateur.username)
    )
    return recrutement, candidatures
