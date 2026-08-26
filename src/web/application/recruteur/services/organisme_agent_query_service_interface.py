from typing import Protocol
from uuid import UUID

from application.recruteur.dtos.agent_organisme_read_models import (
    AgentOrganismeReadModel,
)


class IOrganismeAgentQueryService(Protocol):
    def list_by_organisme(
        self, *, organisme_id: UUID
    ) -> list[AgentOrganismeReadModel]: ...

    def get_one(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeReadModel | None: ...
