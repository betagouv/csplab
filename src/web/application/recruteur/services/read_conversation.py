from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid5

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from application.recruteur.services.list_conversations import stub_conversations_of
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.errors.recrutement_errors import ConversationInexistante
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument

PDF = "application/pdf"
PNG = "image/png"


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


_MESSAGES = [
    (
        "Bonjour, pouvez-vous nous transmettre les pièces de votre dossier ?",
        "Camille Durand",
        datetime(2026, 9, 11, 9, 0, tzinfo=timezone.utc),
        [],
    ),
    (
        "Bonjour, voici mon CV et ma lettre de motivation.",
        "Léa Martin",
        datetime(2026, 9, 12, 10, 30, tzinfo=timezone.utc),
        [
            ("cv.pdf", TypeDocument.CV, PDF, 184_320),
            ("lettre_motivation.pdf", TypeDocument.LETTRE_MOTIVATION, PDF, 42_870),
        ],
    ),
    (
        "Merci. Il nous manque vos justificatifs de diplômes et d'expérience.",
        "Camille Durand",
        datetime(2026, 9, 14, 14, 0, tzinfo=timezone.utc),
        [],
    ),
    (
        "Vous trouverez ci-joint l'ensemble des justificatifs demandés.",
        "Léa Martin",
        datetime(2026, 9, 15, 8, 45, tzinfo=timezone.utc),
        [
            ("diplome_master.pdf", TypeDocument.PIECE_JUSTIFICATIVE, PDF, 512_004),
            ("diplome_licence.pdf", TypeDocument.PIECE_JUSTIFICATIVE, PDF, 498_112),
            (
                "attestation_employeur.pdf",
                TypeDocument.PIECE_JUSTIFICATIVE,
                PDF,
                96_540,
            ),
            ("arrete_nomination.pdf", TypeDocument.PIECE_JUSTIFICATIVE, PDF, 120_310),
            ("piece_identite.png", TypeDocument.AUTRE, PNG, 1_048_576),
        ],
    ),
    (
        "Dossier complet, nous revenons vers vous rapidement.",
        "Nadia Haddad",
        datetime(2026, 9, 17, 11, 10, tzinfo=timezone.utc),
        [],
    ),
    (
        "Vous êtes convoqué(e) à un entretien le 3 octobre à 10h.",
        "Nadia Haddad",
        datetime(2026, 9, 20, 16, 0, tzinfo=timezone.utc),
        [("convocation.pdf", TypeDocument.AUTRE, PDF, 64_200)],
    ),
    (
        "Je confirme ma présence, merci.",
        "Léa Martin",
        datetime(2026, 9, 21, 9, 15, tzinfo=timezone.utc),
        [],
    ),
]


def _check_conversation_belongs_to_candidature(
    candidature_id: UUID, conversation_id: UUID
) -> None:
    if conversation_id not in stub_conversations_of(candidature_id):
        raise ConversationInexistante(conversation_id)


def read_conversation(
    *,
    organisme_id: UUID,
    recrutement_id: UUID,
    candidature_id: UUID,
    conversation_id: UUID,
    utilisateur: Utilisateur,
) -> list[MessageStub]:
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
    service.check_candidature_belongs_to_recrutement(candidature_id)
    _check_conversation_belongs_to_candidature(candidature_id, conversation_id)

    return sorted(
        (
            MessageStub(
                content=contenu,
                author=auteur,
                created_at=created_at,
                documents=[
                    DocumentStub(
                        uuid=uuid5(conversation_id, nom),
                        nom=nom,
                        type=type_document,
                        content_type=content_type,
                        taille=taille,
                    )
                    for nom, type_document, content_type, taille in documents
                ],
            )
            for contenu, auteur, created_at, documents in _MESSAGES
        ),
        key=lambda m: m.created_at,
    )
