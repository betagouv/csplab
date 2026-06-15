from uuid import UUID

from ddd.domain_errors import DomainError


class CandidatInexistant(DomainError):
    def __init__(self, candidat_id: UUID):
        self.candidat_id = candidat_id
        super().__init__(f"Le candidat {candidat_id} n'existe pas")
