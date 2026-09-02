from dataclasses import dataclass
from typing import List

from ddd.usecase_interface import IUsecase

from application.identite.dtos.organisme_read_models import (
    OrganismeReadModel,
)
from application.identite.services.organisme_query_service_interface import (
    IOrganismeQueryService,
)
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class ListOrganismesCommand:
    utilisateur: Utilisateur


class ListOrganismesUsecase(IUsecase[ListOrganismesCommand, List[OrganismeReadModel]]):
    def __init__(
        self,
        organisme_query_service: IOrganismeQueryService,
        permission_service: OrganismePermissionService,
    ):
        self.organisme_query_service = organisme_query_service
        self.permission_service = permission_service

    def can_execute(self, command: ListOrganismesCommand) -> None:
        self.permission_service.est_autorise(
            action=OrganismeAction.LISTER_ORGANISMES,
            utilisateur=command.utilisateur,
        )

    def execute(self, command: ListOrganismesCommand) -> List[OrganismeReadModel]:
        self.can_execute(command)
        return self.organisme_query_service.get_all_with_counts()
