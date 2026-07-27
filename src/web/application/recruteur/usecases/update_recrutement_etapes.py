from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.etape_data import EtapeData
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)


@dataclass(kw_only=True)
class UpdateRecrutementEtapesCommand(RecrutementRequest):
    etapes: list[EtapeData]


# TODO: ajouter
# - RBAC organisme, RBAC recrutement
# - validation coherence des etapes (categories, ordre)
# - recuperer/muter le Recrutement (necessite une methode @mutate sur l'agregat)
# - sauvegarde + emission evenement + drain par auditlog
class UpdateRecrutementEtapesUsecase(
    IUseCase[UpdateRecrutementEtapesCommand, list[EtapeData]]
):
    def __init__(self, organisme_repository: IOrganismeRepository):
        self.organisme_repository = organisme_repository

    def execute(self, command: UpdateRecrutementEtapesCommand) -> list[EtapeData]:
        self.organisme_repository.get_by_id(command.organisme_id)
        return command.etapes
