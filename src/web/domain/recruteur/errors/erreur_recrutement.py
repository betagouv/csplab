from ddd.domain_errors import DomainError


class ErreurRecruteur(DomainError):
    pass


class ConfigurationEtapesInvalide(ErreurRecruteur):
    def __init__(self, raison: str):
        super().__init__(f"Configuration des étapes invalide : {raison}")
        self.raison = raison
