from typing import List, Protocol

from ddd.base_repository_interface import IBaseRepository
from referentiel.types import IUpsertResult

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas

    def upsert_batch(self, organismes: List[Organisme]) -> IUpsertResult: ...
