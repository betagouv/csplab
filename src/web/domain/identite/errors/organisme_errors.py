from domain.exceptions.domain_errors import DomainError


class OrganismeError(DomainError):
    pass


class InvalidSiretError(OrganismeError):
    def __init__(self, siret_str: str):
        super().__init__(f"Invalid SIRET: {siret_str}")
        self.siret_str = siret_str
