from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository
from ddd.page_interface import IPage

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus


class IRecrutementRepository(IBaseRepository[Recrutement], Protocol):
    def filter_by_status(
        self,
        organisme_id: UUID,
        status: RecrutementStatus,
    ) -> IPage[Recrutement]: ...
