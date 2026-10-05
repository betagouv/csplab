from uuid import UUID

from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
)
from infrastructure.django_apps.candidate.models.candidature import CandidatureModel
from infrastructure.django_apps.messagerie.models import ConversationModel


class CandidatureAgentService:
    def __init__(self, *, recrutement_id: UUID, candidature_id: UUID) -> None:
        self.recrutement_id = recrutement_id
        self.candidature_id = candidature_id

    def check_candidature_belongs_to_recrutement(self) -> None:
        if not CandidatureModel.objects.by_recrutement_and_candidature(
            self.recrutement_id, self.candidature_id
        ).exists():
            raise RecrutementCandidatureInexistante(self.candidature_id)

    def check_conversation_belongs_to_candidature(self, conversation_id: UUID) -> None:
        if not ConversationModel.objects.by_candidature_and_id(
            self.candidature_id, conversation_id
        ).exists():
            raise ConversationInexistante(conversation_id)
