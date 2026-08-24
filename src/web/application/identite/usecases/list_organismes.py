from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.usecase_interface import IUseCase
from referentiel.entities.organisme import Organisme

from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class ListOrganismesCommand:
    utilisateur_id: UUID
    est_staff: bool = False


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
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
        )
        return self.organisme_repository.get_all()
