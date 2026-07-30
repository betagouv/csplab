from ddd.domain_errors import DomainError


class OrganismeNexistePas(DomainError):
    def __init__(self, identifier: str):
        super().__init__(f"Organisme introuvable : {identifier}")
        self.identifier = identifier
