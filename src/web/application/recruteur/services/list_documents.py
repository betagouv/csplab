from uuid import UUID

from django.db.models import QuerySet

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.users.models import UserModel


def list_documents(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: UserModel,
) -> QuerySet[DocumentModel]:
    candidature_service = CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )
    candidature_service.check_accessible(PermissionAction.LIST_DOCUMENTS)

    return DocumentModel.objects.by_recrutement_and_candidature(
        recrutement_id, candidature_id
    )
