from ddd.domain_errors import DomainError


class CandidatureError(DomainError):
    pass


class CandidatureNePeutEtreRetiree(CandidatureError):
    def __init__(self, raison: str):
        super().__init__(f"La candidature ne peut pas être retirée : {raison}")


class DossierCandidatureInvalide(CandidatureError):
    def __init__(self, raison: str):
        super().__init__(f"Le dossier de candidature est invalide : {raison}")
