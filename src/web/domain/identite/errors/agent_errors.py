from uuid import UUID

from ddd.domain_errors import DomainError


class AgentError(DomainError):
    pass


class ProfilAgentDoesNotExist(AgentError):
    def __init__(self, entity_id: UUID | str):
        super().__init__(f"Agent profile with ID {entity_id} does not exist")


class ProfilAgentAlreadyExists(AgentError):
    def __init__(self, email: str):
        super().__init__(f"Agent profile with email {email} already exists")
