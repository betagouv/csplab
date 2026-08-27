from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUsecase
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.siret import SIRET
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
class CreateOrganismeCommand:
    nom: str
    versant: Verse
    localisation: Localisation | None
    siret: SIRET | None
    parent_id: UUID | None
    utilisateur: Utilisateur


class CreateOrganismeUsecase(IUsecase[CreateOrganismeCommand, Organisme]):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.permission_service = permission_service

    def can_execute(self, input_data: CreateOrganismeCommand) -> None:
        self.permission_service.est_autorise(
            action=OrganismeAction.CREER_ORGANISME,
            utilisateur=input_data.utilisateur,
        )

    def execute(self, input_data: CreateOrganismeCommand) -> Organisme:
        self.can_execute(input_data=input_data)
        organisme = Organisme.create(
            nom=input_data.nom,
            versant=input_data.versant,
            localisation=input_data.localisation,
            siret=input_data.siret,
            parent_id=input_data.parent_id,
        )
        return self.organisme_repository.create(organisme)
