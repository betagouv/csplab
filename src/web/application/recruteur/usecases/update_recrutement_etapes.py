from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class UpdateRecrutementEtapesCommand(RecrutementRequest):
    etapes: list[EtapeData]


# TODO: ajouter
# - validation coherence des etapes (categories, ordre)
# - recuperer/muter le Recrutement (necessite une methode @mutate sur l'agregat)
# - sauvegarde + emission evenement + drain par auditlog
class UpdateRecrutementEtapesUsecase(
    IUseCase[UpdateRecrutementEtapesCommand, list[EtapeData]]
):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: UpdateRecrutementEtapesCommand) -> list[EtapeData]:
        self.organisme_repository.get_by_id(command.organisme_id)
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            recrutement_id=command.recrutement_id,
            est_staff=command.est_staff,
        )
        return command.etapes
