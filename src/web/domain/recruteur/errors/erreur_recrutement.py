from uuid import UUID

from ddd.domain_errors import DomainError


class ErreurRecruteur(DomainError):
    pass


class CandidatureRecruteurNexistePas(ErreurRecruteur):
    def __init__(self, candidature_id: UUID):
        super().__init__(f"Candidature {candidature_id} does not exist")
        self.candidature_id = candidature_id


class EtapeInvalide(ErreurRecruteur):
    def __init__(self, identifier: str, erreurs: list[str] | None = None):
        details = f" : {', '.join(erreurs)}" if erreurs else ""
        super().__init__(
            f"Etape de recrutement with identifier {identifier} is invalid{details}"
        )
        self.identifier = identifier
