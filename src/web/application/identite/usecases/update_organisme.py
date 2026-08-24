from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.verse import Verse

from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass
class UpdateOrganismeCommand:
    organisme_id: UUID
    name: str | None
    verse: Verse | None
    managed_ats: bool | None
    utilisateur: Utilisateur


class UpdateOrganismeUsecase(IUseCase[UpdateOrganismeCommand, Organisme]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service

    def execute(self, command: UpdateOrganismeCommand) -> Organisme:
        self.permission_service.est_autorise(
            action=OrganismeAction.MODIFIER_ORGANISME,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        organisme = self.organisme_repository.get_by_id(command.organisme_id)
        # todo domain
        # organisme = self.organisme_repository.save(organisme)
        return organisme
