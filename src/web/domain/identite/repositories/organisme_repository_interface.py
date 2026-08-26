from typing import Protocol
from uuid import UUID

from ddd.base_repository_interface import IBaseRepository
from referentiel.entities.organisme import Organisme
from referentiel.types import IUpsertResult
from referentiel.value_objects.siret import SIRET


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas

    def get_ids_by_referentiel_and_external_id(
        self, pairs: list[tuple[str, str]]
    ) -> dict[tuple[str, str], UUID]: ...

    def upsert_batch(self, organismes: list[Organisme]) -> IUpsertResult: ...
