from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.etape_data import EtapeData, etapes_par_defaut
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class GetRecrutementEtapesQuery(RecrutementRequest):
    pass


# TODO: ajouter
# - recuperer le Recrutement via IRecrutementRepository et mapper ses etapes reelles
#   (EtapeRecrutement) vers EtapeData, au lieu du pipeline statique ci-dessous
class GetRecrutementEtapesUsecase(IUseCase[GetRecrutementEtapesQuery, list[EtapeData]]):
    def __init__(
        self,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_permission_service = organisme_permission_service

    def execute(self, query: GetRecrutementEtapesQuery) -> list[EtapeData]:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.GET_RECRUTEMENT_ETAPES,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )
        return etapes_par_defaut()
