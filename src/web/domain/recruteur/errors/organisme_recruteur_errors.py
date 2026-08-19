from ddd.domain_errors import DomainError


class OrganismeRecruteurErreur(DomainError):
    pass


class ConfigurationEtapesInvalide(OrganismeRecruteurErreur):
    def __init__(self, raison: str):
        super().__init__(f"Configuration des étapes invalide : {raison}")
        self.raison = raison
