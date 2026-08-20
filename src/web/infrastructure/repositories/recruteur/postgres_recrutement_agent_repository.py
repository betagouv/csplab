from uuid import UUID

from domain.recruteur.repositories.recrutement_agent_repository_interface import (
    IRecrutementAgentRepository,
)
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)


class PostgresRecrutementAgentRepository(IRecrutementAgentRepository):
    def get_role(
        self, *, recrutement_id: UUID, agent_id: UUID
    ) -> AgentRecrutementRole | None:
        try:
            liaison = RecrutementAgentModel.objects.get(
                recrutement_id=recrutement_id,
                agent_id=agent_id,  # type: ignore[misc]
            )
        except RecrutementAgentModel.DoesNotExist:
            return None
        return AgentRecrutementRole(liaison.role)
