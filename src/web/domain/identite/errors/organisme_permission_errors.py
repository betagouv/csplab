from uuid import UUID

from ddd.domain_errors import DomainError


class PermissionError(DomainError):
    pass


class OperationOrganismeRefusee(PermissionError):
    def __init__(self):
        super().__init__("Seul un membre du staff peut effectuer cette opération")


class OrganismePermissionError(DomainError):
    pass


class AccesOrganismeRefuse(OrganismePermissionError):
    def __init__(self, organisme_id: UUID):
        super().__init__(f"Rôle non autorisé sur l'organisme {organisme_id}")
        self.organisme_id = organisme_id


class AccesRecrutementRefuse(OrganismePermissionError):
    def __init__(self, recrutement_id: UUID):
        super().__init__(f"Rôle non autorisé sur le recrutement {recrutement_id}")
        self.recrutement_id = recrutement_id


class AccesRecrutementInconnu(OrganismePermissionError):
    def __init__(self):
        super().__init__("Recrutement inconnu")
