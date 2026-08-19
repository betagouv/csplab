from ddd.domain_errors import DomainError


class OrganismeError(DomainError):
    pass


class SiretInvalide(OrganismeError):
    def __init__(self, siret_str: str):
        super().__init__(f"Invalid SIRET: {siret_str}")
        self.siret_str = siret_str


class EtablissementInvalideError(OrganismeError):
    def __init__(self, external_id: str, cause: Exception):
        super().__init__(f"Invalid etablissement {external_id}: {cause}")
        self.external_id = external_id
        self.cause = cause
