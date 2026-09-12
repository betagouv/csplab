from dataclasses import dataclass

from ddd.usecase_interface import IUsecase

from application.identite.context_services.organisme_permission_service import (
    can_execute,
)
from application.recruteur.dtos.recrutement_read_models import (
    RecrutementDetailReadModel,
)
from application.recruteur.dtos.recrutement_request import RecrutementRequest
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction


@dataclass(kw_only=True)
class GetRecrutementDetailQuery(RecrutementRequest):
    pass


class GetRecrutementDetailUsecase(
    IUsecase[GetRecrutementDetailQuery, RecrutementDetailReadModel | None]
):
    def __init__(
        self,
        recrutement_query_service: IRecrutementQueryService,
    ):
        self.recrutement_query_service = recrutement_query_service

    def execute(
        self, query: GetRecrutementDetailQuery
    ) -> RecrutementDetailReadModel | None:
        can_execute(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )

        return self.recrutement_query_service.get_detail_by_recrutement(
            organisme_id=query.organisme_id, recrutement_id=query.recrutement_id
        )
