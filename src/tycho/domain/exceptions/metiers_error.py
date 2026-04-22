from domain.exceptions.domain_errors import DomainError


class MetierError(DomainError):
    pass


class MetierDoesNotExist(MetierError):
    def __init__(self, message: str):
        super().__init__(message)
