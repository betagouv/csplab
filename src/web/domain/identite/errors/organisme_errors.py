from ddd.domain_errors import DomainError


class OrganismeError(DomainError):
    pass


class OrganismeSiretExisteDeja(OrganismeError):
    def __init__(self, siret_str: str):
        super().__init__(f"Un organisme avec le siret {siret_str} est déjà enregistré")
        self.siret_str = siret_str
