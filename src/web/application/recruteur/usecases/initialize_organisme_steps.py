from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class InitializeOrganismeStepsCommand:
    organisme_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False


class InitializeOrganismeStepsUsecase(
    IUseCase[InitializeOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_repository: IOrganismeRecruteurRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: InitializeOrganismeStepsCommand) -> OrganismeRecruteur:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.INITIALIZE_ORGANISME_STEPS,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
        )
        organisme = self.organisme_repository.get_by_id(command.organisme_id)
        organisme.initialiser_etapes()
        self.organisme_repository.save(organisme)
        return organisme
