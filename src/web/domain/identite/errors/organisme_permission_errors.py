from ddd.domain_errors import DomainError


class OrganismePermissionError(DomainError):
    pass


class CreationOrganismeRefusee(OrganismePermissionError):
    def __init__(self):
        super().__init__("Seul un membre du staff peut créer un organisme")
