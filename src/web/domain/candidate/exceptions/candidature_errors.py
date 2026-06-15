from uuid import UUID

from ddd.domain_errors import DomainError


class CandidatureError(DomainError):
    pass


class DossierCandidatureInvalide(CandidatureError):
    def __init__(self, raison: str):
        super().__init__(f"Le dossier de candidature est invalide : {raison}")


class CandidatureNexistePas(CandidatureError):
    def __init__(self, candidat_id: UUID, offre_id: UUID):
        super().__init__(
            (f"Pas de candidature pour le candidat {candidat_id} et l'offre {offre_id}")
        )


class CandidatureDejaSoumise(CandidatureError):
    def __init__(self, candidat_id: UUID, offre_id: UUID):
        super().__init__(
            (
                f"Une candidature pour le candidat {candidat_id} "
                f"et l'offre {offre_id} a déjà été soumise"
            )
        )


class OffreInexistante(CandidatureError):
    def __init__(self, offre_id: UUID):
        self.offre_id = offre_id
        super().__init__(f"L'offre {offre_id} n'existe pas")


class CandidatInexistant(CandidatureError):
    def __init__(self, candidat_id: UUID):
        self.candidat_id = candidat_id
        super().__init__(f"Le candidat {candidat_id} n'existe pas")
