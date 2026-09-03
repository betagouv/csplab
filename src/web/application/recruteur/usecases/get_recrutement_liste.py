from dataclasses import dataclass

from ddd.page_interface import IPage
from ddd.usecase_interface import IUsecase

from application.recruteur.dtos.recrutement_read_models import (
    CandidatureListeReadModel,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class GetRecrutementListeQuery(RecrutementRequest):
    pass


class GetRecrutementListeUsecase(
    IUsecase[GetRecrutementListeQuery, IPage[CandidatureListeReadModel] | None]
):
    def __init__(
        self,
        organisme_permission_service: OrganismePermissionService,
        recrutement_query_service: IRecrutementQueryService,
    ):
        self.organisme_permission_service = organisme_permission_service
        self.recrutement_query_service = recrutement_query_service

    def can_execute(self, query: GetRecrutementListeQuery) -> None:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )

    def execute(
        self, query: GetRecrutementListeQuery
    ) -> IPage[CandidatureListeReadModel] | None:
        self.can_execute(query)
        return self.recrutement_query_service.get_candidatures_by_recrutement(
            organisme_id=query.organisme_id, recrutement_id=query.recrutement_id
        )
