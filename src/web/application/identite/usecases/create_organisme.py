from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.value_objects.siret import SIRET


@dataclass
class CreateOrganismeCommand:
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET | None
    parent_id: UUID | None


class CreateOrganismeUsecase(IUseCase[CreateOrganismeCommand, Organisme]):
    def __init__(self, organisme_repository: IOrganismeRepository):
        self.organisme_repository = organisme_repository

    def execute(self, input_data: CreateOrganismeCommand) -> Organisme:
        organisme = Organisme.create(
            nom=input_data.nom,
            versant=input_data.versant,
            localisation=input_data.localisation,
            siret=input_data.siret,
            parent_id=input_data.parent_id,
        )
        return self.organisme_repository.create(organisme)
