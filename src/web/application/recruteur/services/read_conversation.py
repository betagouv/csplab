import logging
from uuid import UUID, uuid4

from django.db import DatabaseError, transaction
from django.db.models import QuerySet
from django.utils import timezone

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
from infrastructure.django_apps.messagerie.models import (
    ConversationLectureModel,
    MessageModel,
)

logger = logging.getLogger(__name__)


def mark_as_read(*, conversation_id: UUID, utilisateur: Utilisateur) -> None:
    try:
        with transaction.atomic():
            now = timezone.now()
            ConversationLectureModel.objects.update_or_create(
                conversation_id=conversation_id,
                utilisateur_id=utilisateur.entity_id,
                defaults={"read_at": now},
                create_defaults={"id": uuid4(), "read_at": now},
            )
    except DatabaseError:
        logger.exception(
            "Could not mark conversation %s as read for %s",
            conversation_id,
            utilisateur.entity_id,
        )


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

    mark_as_read(conversation_id=conversation_id, utilisateur=utilisateur)

    return MessageModel.objects.by_conversation(conversation_id)
