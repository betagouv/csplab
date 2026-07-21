from uuid import UUID

from ddd.domain_errors import DomainError


class OrganismePermissionError(DomainError):
    pass


class AccesOrganismeRefuse(OrganismePermissionError):
    def __init__(self, organisme_id: UUID):
        super().__init__(f"Rôle non autorisé sur l'organisme {organisme_id}")
        self.organisme_id = organisme_id
