from uuid import UUID, uuid4

from ddd.entity import Entity
from django.core.files.uploadedfile import UploadedFile
from django.db import transaction

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


def create_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    objet: str,
    content: str,
    documents: list[UploadedFile],
    utilisateur: Utilisateur,
) -> ConversationModel:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_CONVERSATION,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    contexte = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    contexte.check_recrutement_belongs_to_organisme()
    candidature_service = CandidatureAgentService(
        recrutement_id=recrutement_id, candidature_id=candidature_id
    )
    candidature_service.check_candidature_belongs_to_recrutement()

    auteur_id = utilisateur.entity_id

    with transaction.atomic():
        conversation = ConversationModel.objects.create(
            id=uuid4(), candidature_id=candidature_id, objet=objet
        )
        message = MessageModel.objects.create(
            id=uuid4(),
            conversation=conversation,
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
            entity=Entity(entity_id=conversation.id),
            ressource_kind="Conversation",
            event_name="ConversationCreee",
        )

    return ConversationModel.objects.by_candidature(candidature_id).get(
        pk=conversation.id
    )
