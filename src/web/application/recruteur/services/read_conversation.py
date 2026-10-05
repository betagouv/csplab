from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from django.db.models import QuerySet

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.messagerie.models import MessageModel


@dataclass(frozen=True, kw_only=True)
class DocumentStub:
    uuid: UUID
    nom: str
    type: str
    content_type: str
    taille: int


@dataclass(frozen=True, kw_only=True)
class MessageStub:
    content: str
    author: str
    created_at: datetime
    documents: list[DocumentStub]


def read_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    conversation_id: UUID,
    utilisateur: Utilisateur,
) -> QuerySet[MessageModel]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.READ_CONVERSATION,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    service = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    service.check_recrutement_belongs_to_organisme()
    candidature_service = CandidatureAgentService(
        recrutement_id=recrutement_id, candidature_id=candidature_id
    )
    candidature_service.check_candidature_belongs_to_recrutement()
    candidature_service.check_conversation_belongs_to_candidature(conversation_id)

    return MessageModel.objects.by_conversation(conversation_id)
