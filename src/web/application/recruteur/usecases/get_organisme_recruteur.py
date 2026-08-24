from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)


@dataclass
class GetOrganismeRecruteurQuery:
    organisme_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False


class GetOrganismeRecruteurUsecase(
    IUseCase[GetOrganismeRecruteurQuery, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: GetOrganismeRecruteurQuery) -> OrganismeRecruteur:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            est_staff=command.est_staff,
        )
        return self.organisme_recruteur_repository.get_by_id(command.organisme_id)
