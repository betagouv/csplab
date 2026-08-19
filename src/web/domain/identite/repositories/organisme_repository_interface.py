from typing import Protocol

from ddd.base_repository_interface import IBaseRepository

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas
