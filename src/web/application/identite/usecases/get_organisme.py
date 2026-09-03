from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase
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
class GetOrganismeCommand:
    organisme_id: UUID
    utilisateur: Utilisateur


class GetOrganismeUsecase(IUsecase[GetOrganismeCommand, Organisme]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service

    def execute(self, command: GetOrganismeCommand) -> Organisme:
        self.permission_service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        return self.organisme_repository.get_by_id(command.organisme_id)
