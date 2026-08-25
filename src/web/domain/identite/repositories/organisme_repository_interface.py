from typing import Protocol

from ddd.base_repository_interface import IBaseRepository
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.siret import SIRET


class IOrganismeRepository(IBaseRepository[Organisme], Protocol):
    def get_by_siret(self, siret: SIRET) -> Organisme: ...  # raises OrganismeNexistePas

    def get_by_referentiel_and_external_id(
        self, referentiel: str, external_id: str
    ) -> Organisme | None: ...
