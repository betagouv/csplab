from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


@dataclass(frozen=True)
class EtapeInput:
    nom: str
    categorie: CategorieEtapeRecrutement
    etape_uuid: UUID | None = None


@dataclass(frozen=True)
class UpdateOrganismeStepsCommand:
    organisme_id: UUID
    etapes: tuple[EtapeInput, ...]


class UpdateOrganismeStepsUsecase(
    IUseCase[UpdateOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(self, organisme_repository: IOrganismeRecruteurRepository) -> None:
        self.organisme_repository = organisme_repository

    def execute(self, command: UpdateOrganismeStepsCommand) -> OrganismeRecruteur:
        organisme = self.organisme_repository.get_by_id(command.organisme_id)
        etapes = tuple(self._to_etape(etape_input) for etape_input in command.etapes)
        organisme.modifier_etapes(etapes=etapes)
        self.organisme_repository.save(organisme)
        return organisme

    @staticmethod
    def _to_etape(etape_input: EtapeInput) -> EtapeRecrutement:
        if etape_input.etape_uuid is not None:
            return EtapeRecrutement.build(
                entity_id=etape_input.etape_uuid,
                categorie=etape_input.categorie,
                nom=etape_input.nom,
            )
        return EtapeRecrutement.create(
            categorie=etape_input.categorie,
            nom=etape_input.nom,
        )
