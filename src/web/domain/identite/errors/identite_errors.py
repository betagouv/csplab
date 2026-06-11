from uuid import UUID

from ddd.domain_errors import DomainError


class UtilisateurDoesNotExist(DomainError):
    def __init__(self, entity_id: UUID | str):
        super().__init__(f"User with ID {entity_id} does not exist")
