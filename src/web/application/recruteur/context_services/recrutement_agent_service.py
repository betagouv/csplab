from uuid import UUID

from domain.recruteur.errors.organisme_agent_errors import AgentNonRattache
from domain.recruteur.errors.recrutement_agent_errors import (
    AgentDejaMembreRecrutement,
    AgentNonMembreRecrutement,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentInexistant,
    RecrutementInexistant,
)
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
    RecrutementModel,
)


class RecrutementAgentService:
    def __init__(self, *, organisme_id: UUID, recrutement_id: UUID) -> None:
        self.organisme_id = organisme_id
        self.recrutement_id = recrutement_id

    def check_recrutement_belongs_to_organisme(self) -> None:
        if not RecrutementModel.objects.by_organisme_and_recrutement(
            self.organisme_id, self.recrutement_id
        ).exists():
            raise RecrutementInexistant(self.recrutement_id)

    def check_document_belongs_to_recrutement(
        self, candidature_id: UUID, document_id: UUID
    ) -> None:
        if not DocumentModel.objects.by_recrutement_candidature_and_document(
            self.recrutement_id, candidature_id, document_id
        ).exists():
            raise RecrutementDocumentInexistant(document_id)

    def check_agent_attached_to_organisme(self, agent_id: UUID) -> None:
        if not OrganismeAgentModel.objects.by_organisme_and_agent(
            self.organisme_id, agent_id
        ).exists():
            raise AgentNonRattache(self.organisme_id, agent_id)

    def check_agent_not_active_member(self, agent_id: UUID) -> None:
        if RecrutementAgentModel.objects.by_recrutement_and_agent(
            self.recrutement_id, agent_id
        ).exists():
            raise AgentDejaMembreRecrutement(self.recrutement_id, agent_id)

    def get_active_member(self, agent_id: UUID) -> RecrutementAgentModel:
        try:
            return RecrutementAgentModel.objects.by_recrutement_and_agent(
                self.recrutement_id, agent_id
            ).get()
        except RecrutementAgentModel.DoesNotExist as error:
            raise AgentNonMembreRecrutement(self.recrutement_id, agent_id) from error
