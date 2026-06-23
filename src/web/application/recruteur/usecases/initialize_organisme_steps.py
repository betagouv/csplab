from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)


@dataclass
class InitializeOrganismeStepsCommand:
    organisme_id: UUID


class InitializeOrganismeStepsUsecase(
    IUseCase[InitializeOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(self, organisme_repository: IOrganismeRecruteurRepository):
        self.organisme_repository = organisme_repository

    def execute(self, command: InitializeOrganismeStepsCommand) -> OrganismeRecruteur:
        organisme = self.organisme_repository.get_by_id(command.organisme_id)
        organisme.initialiser_etapes()
        self.organisme_repository.save(organisme)
        return organisme
