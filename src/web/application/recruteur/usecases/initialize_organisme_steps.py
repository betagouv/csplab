from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)


@dataclass
class InitializeOrganismeStepsCommand:
    organisme_id: UUID
    utilisateur: Utilisateur


class InitializeOrganismeStepsUsecase(
    IUsecase[InitializeOrganismeStepsCommand, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: InitializeOrganismeStepsCommand) -> OrganismeRecruteur:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.INITIALIZE_ORGANISME_STEPS,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        organisme = self.organisme_recruteur_repository.get_by_id(command.organisme_id)
        organisme.initialiser_etapes()
        self.organisme_recruteur_repository.save(organisme)
        return organisme
