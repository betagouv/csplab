from domain.exceptions.domain_errors import DomainError


class CandidatureError(DomainError):
    pass


class CandidatureNePeutPasEtreSoumise(CandidatureError):
    def __init__(self, raison: str):
        super().__init__(f"La candidature ne peut pas être créée ou soumise : {raison}")


class DossierCandidatureInvalide(CandidatureError):
    def __init__(self, raison: str):
        super().__init__(f"Le dossier de candidature est invalide : {raison}")


class CandidatureNePeutEtreRetiree(CandidatureError):
    def __init__(self):
        super().__init__("Seules les candidatures soumises peuvent être retirées")
