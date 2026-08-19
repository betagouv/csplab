from typing import List, Protocol, TypedDict

from ddd.base_repository_interface import IBaseRepository
from referentiel.types import IUpsertError

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET


class IOrganismeUpsertResult(TypedDict):
    created: int
    updated: int
    errors: List[IUpsertError]
    created_organismes: List[Organisme]
    updated_organismes: List[Organisme]


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas

    def upsert_batch(self, organismes: List[Organisme]) -> IOrganismeUpsertResult: ...
