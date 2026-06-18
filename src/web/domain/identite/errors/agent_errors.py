from uuid import UUID

from ddd.domain_errors import DomainError


class AgentError(DomainError):
    pass


class ProfilAgentNexistePas(AgentError):
    def __init__(self, entity_id: UUID | str):
        super().__init__(f"Agent profile with ID {entity_id} does not exist")


class ProfilAgentExisteDeja(AgentError):
    def __init__(self, email: str):
        super().__init__(f"Agent profile with email {email} already exists")
