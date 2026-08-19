from ddd.domain_errors import DomainError


class PermissionError(DomainError):
    pass


class OperationOrganismeRefusee(PermissionError):
    def __init__(self):
        super().__init__("Seul un membre du staff peut effectuer cette opération")


class CreationOrganismeRefusee(PermissionError):
    def __init__(self):
        super().__init__("Seul un membre du staff peut créer un organisme")
