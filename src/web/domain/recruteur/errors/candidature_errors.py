from uuid import UUID

from ddd.domain_errors import DomainError


class CandidatureRecruteurError(DomainError):
    pass


class CandidatureInexistante(CandidatureRecruteurError):
    def __init__(self, candidature_id: UUID):
        super().__init__((f"Candidature {candidature_id} inexistante"))
