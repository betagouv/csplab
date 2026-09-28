from uuid import UUID

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from application.recruteur.services.list_conversations import (
    ConversationStub,
    stub_conversation_id,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction


def create_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    objet: str,
    content: str,
    documents: list[UploadedFile],
    utilisateur: Utilisateur,
) -> ConversationStub:
    """Stub : rien n'est persisté, les documents sont ignorés."""
    OrganismePermissionService().can_execute(
        action=OrganismeAction.CREATE_CONVERSATION,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    service = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    service.check_recrutement_belongs_to_organisme()
    service.check_candidature_belongs_to_recrutement(candidature_id)

    auteur = f"{utilisateur.prenom} {utilisateur.nom}".strip()
    now = timezone.now()
    return ConversationStub(
        uuid=stub_conversation_id(candidature_id, objet),
        objet=objet,
        creator=auteur,
        created_at=now,
        last_message_content=content[
            : settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH
        ],
        last_message_author=auteur,
        last_message_created_at=now,
    )
