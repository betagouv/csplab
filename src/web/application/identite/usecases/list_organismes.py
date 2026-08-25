from dataclasses import dataclass
from typing import List

from ddd.usecase_interface import IUseCase
from referentiel.entities.organisme import Organisme

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class ListOrganismesCommand:
    utilisateur: Utilisateur


class ListOrganismesUsecase(IUseCase[ListOrganismesCommand, List[Organisme]]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service

    def execute(self, command: ListOrganismesCommand) -> List[Organisme]:
        self.permission_service.est_autorise(
            action=OrganismeAction.LISTER_ORGANISMES,
            utilisateur=command.utilisateur,
        )
        return self.organisme_repository.get_all()
