from uuid import UUID

from ddd.domain_errors import DomainError


class OrganismeAgentError(DomainError):
    pass


class AgentDejaRattache(OrganismeAgentError):
    def __init__(self, organisme_id: UUID, agent_id: UUID):
        super().__init__(
            f"Agent {agent_id} is already attached to organisme {organisme_id}"
        )
        self.organisme_id = organisme_id
        self.agent_id = agent_id
