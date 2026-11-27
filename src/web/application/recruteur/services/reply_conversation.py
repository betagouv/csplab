from uuid import UUID, uuid4

from ddd.entity import Entity
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.value_objects.permission_action import PermissionAction
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.messagerie.models import (
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def reply_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    conversation_id: UUID,
    content: str,
    documents: list[UploadedFile],
    utilisateur: UserModel,
) -> MessageModel:
    candidature_service = CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )
    candidature_service.check_accessible(PermissionAction.REPLY_CONVERSATION)
    candidature_service.check_conversation_belongs_to_candidature(conversation_id)

    auteur_id = utilisateur.username

    with transaction.atomic():
        message = MessageModel.objects.create(
            id=uuid4(),
            conversation_id=conversation_id,
            auteur_id=auteur_id,
            contenu=content,
        )
        attachements = DocumentModel.objects.bulk_create(
            DocumentModel.objects.build_from_upload(
                upload, candidature_id=candidature_id, depose_par_id=auteur_id
            )
            for upload in documents
        )
        MessageDocumentModel.objects.bulk_create(
            MessageDocumentModel(id=uuid4(), message=message, document=document)
            for document in attachements
        )
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=auteur_id,
            entity=Entity(entity_id=message.id),
            ressource_kind="Message",
            event_name="MessageCree",
        )

    return MessageModel.objects.by_conversation(conversation_id).get(pk=message.id)
