from uuid import UUID

from ddd.domain_errors import DomainError


class RecrutementError(DomainError):
    pass


class RecrutementInexistant(RecrutementError):
    def __init__(self, recrutement_id: UUID):
        super().__init__((f"{recrutement_id} inexistant"))


class RecrutementCandidatureInexistante(RecrutementError):
    def __init__(self, candidature_id: UUID, recrutement_id: UUID):
        super().__init__(
            (
                f"Candidature {candidature_id} inexistante pour ce recrutement"
                f" {recrutement_id}"
            )
        )


class RecrutementEtapeInexistante(RecrutementError):
    def __init__(self, etape_id: UUID, recrutement_id: UUID):
        super().__init__(
            (f"Etape {etape_id} inexistante pour ce recrutement {recrutement_id}")
        )
