from typing import Protocol
from uuid import UUID

from domain.recruteur.value_objects.roles import AgentOrganismeRole


class IOrganismeAgentRepository(Protocol):
    def get_role(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeRole | None: ...
