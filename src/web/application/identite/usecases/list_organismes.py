from dataclasses import dataclass
from typing import List
from uuid import UUID

from ddd.usecase_interface import IUseCase
from referentiel.entities.organisme import Organisme

from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.identite_permission_service import (
    OrganismeCreationPermissionService,
)


@dataclass
class ListOrganismesCommand:
    user_id: UUID


class ListOrganismeUsecase(IUseCase[ListOrganismesCommand, List[Organisme]]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismeCreationPermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service

    def execute(self, command: ListOrganismesCommand) -> List[Organisme]:
        # todo
        # self.permission_service.est_autorise()
        return self.organisme_repository.get_all()
