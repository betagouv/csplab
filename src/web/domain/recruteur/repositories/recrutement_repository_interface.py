from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository
from ddd.page_interface import IPage

from domain.recruteur.entities.recrutement import Recrutement


class IRecrutementRepository(IBaseRepository[Recrutement], Protocol):
    def get_by_organisme(self, organisme_id: UUID):
        IPage[Recrutement]
