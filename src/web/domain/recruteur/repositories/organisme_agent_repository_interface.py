from datetime import datetime
from typing import Protocol
from uuid import UUID

from domain.recruteur.value_objects.roles import AgentOrganismeRole


class IOrganismeAgentRepository(Protocol):
    def get_role(
        self, *, organisme_id: UUID, agent_id: UUID
    ) -> AgentOrganismeRole | None: ...

    def attach(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None: ...

    def is_revoked(self, *, organisme_id: UUID, agent_id: UUID) -> bool | None: ...

    def reattach(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None: ...

    def update_role(
        self, *, organisme_id: UUID, agent_id: UUID, role: AgentOrganismeRole
    ) -> None: ...

    def revoke(
        self, *, organisme_id: UUID, agent_id: UUID, date_revocation: datetime
    ) -> None: ...
