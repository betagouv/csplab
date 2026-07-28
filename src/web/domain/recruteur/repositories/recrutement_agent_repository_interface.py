from typing import Protocol
from uuid import UUID

from domain.recruteur.value_objects.roles import AgentRecrutementRole


class IRecrutementAgentRepository(Protocol):
    def get_role(
        self, *, recrutement_id: UUID, agent_id: UUID
    ) -> AgentRecrutementRole | None: ...
