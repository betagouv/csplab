from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid5

from django.conf import settings

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass(frozen=True, kw_only=True)
class ConversationStub:
    uuid: UUID
    objet: str
    creator: str
    created_at: datetime
    last_message_content: str
    last_message_author: str
    last_message_created_at: datetime


_CONVERSATIONS = [
    (
        "Convocation à l'entretien",
        "Camille Durand",
        datetime(2026, 9, 19, 9, 30, tzinfo=timezone.utc),
        "Bonjour, pouvez-vous confirmer votre présence le 3 octobre à 10h ?",
        "Camille Durand",
        datetime(2026, 9, 22, 14, 5, tzinfo=timezone.utc),
    ),
    (
        "Pièces justificatives",
        "Nadia Haddad",
        datetime(2026, 9, 15, 10, 0, tzinfo=timezone.utc),
        "Merci de nous transmettre votre dernier arrêté de nomination. " * 10,
        "Nadia Haddad",
        datetime(2026, 9, 20, 16, 45, tzinfo=timezone.utc),
    ),
    (
        "Question sur le poste",
        "Léa Martin",
        datetime(2026, 9, 16, 8, 15, tzinfo=timezone.utc),
        "Le poste est-il ouvert au télétravail ?",
        "Nadia Haddad",
        datetime(2026, 9, 17, 11, 20, tzinfo=timezone.utc),
    ),
    (
        "Accusé de réception",
        "Sami Benali",
        datetime(2026, 9, 13, 9, 0, tzinfo=timezone.utc),
        "Nous avons bien reçu votre candidature.",
        "Sami Benali",
        datetime(2026, 9, 13, 9, 0, tzinfo=timezone.utc),
    ),
]


def stub_conversation_id(candidature_id: UUID, objet: str) -> UUID:
    return uuid5(candidature_id, objet)


def stub_conversations_of(candidature_id: UUID) -> dict[UUID, ConversationStub]:
    conversations = (
        ConversationStub(
            uuid=stub_conversation_id(candidature_id, objet),
            objet=objet,
            creator=createur,
            created_at=created_at,
            last_message_content=contenu[
                : settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH
            ],
            last_message_author=auteur,
            last_message_created_at=last_message_created_at,
        )
        for (
            objet,
            createur,
            created_at,
            contenu,
            auteur,
            last_message_created_at,
        ) in _CONVERSATIONS
    )
    return {conversation.uuid: conversation for conversation in conversations}


def list_conversations(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    utilisateur: Utilisateur,
) -> list[ConversationStub]:
    OrganismePermissionService().can_execute(
        action=OrganismeAction.LIST_CONVERSATIONS,
        utilisateur=utilisateur,
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
    )
    service = RecrutementAgentService(
        organisme_id=organisme_id, recrutement_id=recrutement_id
    )
    service.check_recrutement_belongs_to_organisme()
    service.check_candidature_belongs_to_recrutement(candidature_id)

    return sorted(
        stub_conversations_of(candidature_id).values(),
        key=lambda c: c.last_message_created_at,
        reverse=True,
    )
