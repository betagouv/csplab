from typing import Protocol

from ddd.base_repository_interface import IBaseRepository
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.siret import SIRET


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas
