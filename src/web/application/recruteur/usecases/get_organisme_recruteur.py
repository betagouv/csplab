from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from domain.identite.entities.utilisateurs import Utilisateur
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
    ):
        self.organisme_recruteur_repository = organisme_recruteur_repository

    def execute(self, command: GetOrganismeRecruteurQuery) -> OrganismeRecruteur:
        can_execute(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=command.organisme_id,
            utilisateur=command.utilisateur,
        )
        return self.organisme_recruteur_repository.get_by_id(command.organisme_id)
