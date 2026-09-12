from uuid import UUID

from ddd.domain_errors import DomainError


class RecrutementAgentError(DomainError):
    pass


class AgentDejaMembreRecrutement(RecrutementAgentError):
    def __init__(self, recrutement_id: UUID, agent_id: UUID):
        super().__init__(
            f"Agent {agent_id} is already a member of recrutement {recrutement_id}"
        )
        self.recrutement_id = recrutement_id
        self.agent_id = agent_id
