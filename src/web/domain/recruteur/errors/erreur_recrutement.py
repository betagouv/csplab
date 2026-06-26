from ddd.domain_errors import DomainError


class ErreurRecruteur(DomainError):
    pass


class OrganismeRecruteurIntrouvable(ErreurRecruteur):
    def __init__(self, organisme_id):
        super().__init__(
            f"Organisme recruteur avec l'identifiant {organisme_id} non trouvé"
        )
        self.organisme_id = organisme_id


class EtapeInvalide(ErreurRecruteur):
    def __init__(self, identifier: str, erreurs: list[str] | None = None):
        details = f" : {', '.join(erreurs)}" if erreurs else ""
        super().__init__(
            f"Etape de recrutement with identifier {identifier} is invalid{details}"
        )
        self.identifier = identifier
