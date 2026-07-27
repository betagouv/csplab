from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.etape_data import EtapeData, etapes_par_defaut
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)


@dataclass(kw_only=True)
class InitRecrutementEtapesCommand(RecrutementRequest):
    pass


# TODO: ajouter
# - RBAC organisme, RBAC recrutement
# - copier les etapes par defaut de l'organisme sur ce recrutement (au lieu du
#   pipeline statique ci-dessous), sauvegarde + emission evenement + audit log
class InitRecrutementEtapesUsecase(
    IUseCase[InitRecrutementEtapesCommand, list[EtapeData]]
):
    def __init__(self, organisme_repository: IOrganismeRepository):
        self.organisme_repository = organisme_repository

    def execute(self, command: InitRecrutementEtapesCommand) -> list[EtapeData]:
        self.organisme_repository.get_by_id(command.organisme_id)
        return etapes_par_defaut()
