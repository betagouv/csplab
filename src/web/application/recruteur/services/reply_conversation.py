from uuid import UUID, uuid5

from django.core.files.uploadedfile import UploadedFile
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
from application.recruteur.services.read_conversation import (
    DocumentStub,
    MessageStub,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument


def _document_stub(conversation_id: UUID, document: UploadedFile) -> DocumentStub:
    nom = document.name or ""
    return DocumentStub(
        uuid=uuid5(conversation_id, nom),
        nom=nom,
        type=TypeDocument.AUTRE,
        content_type=document.content_type or "",
        taille=document.size or 0,
    )


def reply_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    conversation_id: UUID,
    content: str,
    documents: list[UploadedFile],
    utilisateur: Utilisateur,
) -> MessageStub:
    """Stub : rien n'est persisté."""
    OrganismePermissionService().can_execute(
        action=OrganismeAction.REPLY_CONVERSATION,
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

    return MessageStub(
        content=content,
        author=f"{utilisateur.prenom} {utilisateur.nom}".strip(),
        created_at=timezone.now(),
        documents=[_document_stub(conversation_id, document) for document in documents],
    )
