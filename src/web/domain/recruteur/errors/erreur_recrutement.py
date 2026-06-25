from uuid import UUID

from ddd.domain_errors import DomainError


class ErreurRecruteur(DomainError):
    pass


class EtapeInvalide(ErreurRecruteur):
    def __init__(self, identifier: str, erreurs: list[str] | None = None):
        details = f" : {', '.join(erreurs)}" if erreurs else ""
        super().__init__(
            f"Etape de recrutement with identifier {identifier} is invalid {details}"
        )
        self.identifier = identifier


class CandidatureDejaPresente(ErreurRecruteur):
    def __init__(self, candidature_id: UUID):
        super().__init__(
            f"Candidature {candidature_id} is already present in this recrutement"
        )
        self.candidature_id = candidature_id
