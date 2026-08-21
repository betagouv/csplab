from uuid import UUID

from ddd.domain_errors import DomainError


class RecrutementError(DomainError):
    pass


class RecrutementInexistant(RecrutementError):
    def __init__(self, recrutement_id: UUID):
        super().__init__(f"{recrutement_id} inexistant")


class RecrutementCandidatureInexistante(RecrutementError):
    def __init__(self, candidature_id: UUID):
        super().__init__(
            (f"La candidature {candidature_id} ne correspond pas à ce recrutement")
        )


class RecrutementEtapeInexistante(RecrutementError):
    def __init__(self, etape_id: UUID, recrutement_id: UUID):
        super().__init__(
            f"Etape {etape_id} inexistante pour ce recrutement {recrutement_id}"
        )


class CandidatureInexistante(RecrutementError):
    def __init__(self, candidature_id: UUID):
        super().__init__((f"Candidature {candidature_id} inexistante"))


class SupressionEtapeImpossible(RecrutementError):
    def __init__(self, etape_id: UUID, nombre_candidatures: int):
        super().__init__(
            f"L'étape {etape_id} ne peut être supprimée "
            f"car {nombre_candidatures} candidature"
            f"{'s sont' if nombre_candidatures > 1 else ' est'} en cours"
        )
