from domain.exceptions.domain_errors import DomainError


class EtapeRecrutementInvalide(DomainError):
    def __init__(self, identifier: str, erreurs: list[str] | None = None):
        details = f" : {', '.join(erreurs)}" if erreurs else ""
        super().__init__(
            f"Etape de recrutement with identifier {identifier} is invalid{details}"
        )
        self.identifier = identifier
