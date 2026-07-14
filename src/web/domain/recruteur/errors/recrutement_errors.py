from uuid import UUID

from ddd.domain_errors import DomainError


class RecrutementError(DomainError):
    pass


class RecrutementInexistant(RecrutementError):
    def __init__(self, recrutement_id: UUID):
        super().__init__((f"{recrutement_id} inexistant"))
