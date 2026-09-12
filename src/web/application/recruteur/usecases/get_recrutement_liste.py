from dataclasses import dataclass

from ddd.page_interface import IPage
from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.recrutement_read_models import (
    CandidatureListeReadModel,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
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
        recrutement_query_service: IRecrutementQueryService,
    ):
        self.recrutement_query_service = recrutement_query_service

    def execute(
        self, query: GetRecrutementListeQuery
    ) -> IPage[CandidatureListeReadModel] | None:
        can_execute(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )

        return self.recrutement_query_service.get_candidatures_by_recrutement(
            organisme_id=query.organisme_id, recrutement_id=query.recrutement_id
        )
