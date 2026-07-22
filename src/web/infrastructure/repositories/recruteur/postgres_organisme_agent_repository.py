from uuid import UUID

from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel


class PostgresOrganismeAgentRepository(IOrganismeAgentRepository):
    def get_role(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeRole | None:
        try:
            liaison = OrganismeAgentModel.objects.get(
                organisme_id=organisme_id,
                agent_id=str(agent_id),  # type: ignore[misc]
            )
        except OrganismeAgentModel.DoesNotExist:
            return None
        return AgentOrganismeRole(liaison.role)
