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
class GetOrganismeRecruteurQuery:
    organisme_id: UUID
    utilisateur: Utilisateur


class GetOrganismeRecruteurUsecase(
    IUsecase[GetOrganismeRecruteurQuery, OrganismeRecruteur]
):
    def __init__(
        self,
        organisme_recruteur_repository: IOrganismeRecruteurRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository
        self.organisme_permission_service = organisme_permission_service

    def can_execute(self, command: GetOrganismeRecruteurQuery) -> None:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )

    def execute(self, command: GetOrganismeRecruteurQuery) -> OrganismeRecruteur:
        self.can_execute(command=command)
        return self.organisme_recruteur_repository.get_by_id(command.organisme_id)
