import os
from datetime import timedelta
from uuid import uuid4

from ddd.entity import Entity
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageModel,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

DEMO_CANDIDATE_REPLY = (
    "Je suis un candidat fictif. Je réponds à votre message pour que vous "
    "puissiez avoir une expérience complète de l'activité messagerie."
)


def reply_as_demo_candidates() -> int:
    if os.environ.get("SCALEWAY_ENV") == "prod":
        return 0
    delay = timedelta(minutes=settings.DEMO_AUTO_REPLY_DELAY_MINUTES)
    conversations = (
        ConversationModel.objects.of_demo_candidates().awaiting_candidate_reply(
            timezone.now() - delay
        )
    )

    replies = 0
    for conversation in conversations:
        with transaction.atomic():
            message = MessageModel.objects.create(
                id=uuid4(),
                conversation_id=conversation.pk,
                auteur_id=conversation.candidat_id,
                contenu=DEMO_CANDIDATE_REPLY,
            )
            AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
                utilisateur_id=conversation.candidat_id,
                entity=Entity(entity_id=message.id),
                ressource_kind="Message",
                event_name="MessageCree",
            )
        replies += 1
    return replies
