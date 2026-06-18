from ddd.domain_errors import DomainError


class OrganismeError(DomainError):
    pass


class SiretInvalide(OrganismeError):
    def __init__(self, siret_str: str):
        super().__init__(f"Invalid SIRET: {siret_str}")
        self.siret_str = siret_str


class OrganismeNexistePas(OrganismeError):
    def __init__(self, identifier: str):
        super().__init__(f"Organisme introuvable : {identifier}")
        self.identifier = identifier
