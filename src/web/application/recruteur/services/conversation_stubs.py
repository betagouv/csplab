from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid5

from django.conf import settings


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
