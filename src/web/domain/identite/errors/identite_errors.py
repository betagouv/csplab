from uuid import UUID

from ddd.domain_errors import DomainError


class UtilisateurNexistePas(DomainError):
    def __init__(self, entity_id: UUID | str):
        super().__init__(f"User with ID {entity_id} does not exist")


class UtilisateurExisteDeja(DomainError):
    def __init__(self, entity_id: UUID | str):
        super().__init__(f"User with ID {entity_id} already exists")
