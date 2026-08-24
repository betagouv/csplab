from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.etape_data import EtapeData, etapes_par_defaut
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class InitRecrutementEtapesCommand(RecrutementRequest):
    pass


# TODO: ajouter
# - copier les etapes par defaut de l'organisme sur ce recrutement (au lieu du
#   pipeline statique ci-dessous), sauvegarde + emission evenement + audit log
class InitRecrutementEtapesUsecase(
    IUseCase[InitRecrutementEtapesCommand, list[EtapeData]]
):
    def __init__(
        self,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_permission_service = organisme_permission_service

    def execute(self, command: InitRecrutementEtapesCommand) -> list[EtapeData]:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.INIT_RECRUTEMENT_ETAPES,
            organisme_id=command.organisme_id,
            agent_id=command.utilisateur_id,
            recrutement_id=command.recrutement_id,
            est_staff=command.est_staff,
        )
        return etapes_par_defaut()
