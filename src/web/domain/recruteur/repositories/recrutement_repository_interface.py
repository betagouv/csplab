from typing import Protocol
from uuid import UUID

from domain.recruteur.entities.recrutement import Recrutement


class IRecrutementRepository(Protocol):
    def get_by_id(self, aggregate_id: UUID) -> Recrutement: ...
