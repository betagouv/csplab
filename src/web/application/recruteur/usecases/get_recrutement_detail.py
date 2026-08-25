from dataclasses import dataclass

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.recrutement_read_models import (
    RecrutementDetailReadModel,
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
class GetRecrutementDetailQuery(RecrutementRequest):
    pass


class GetRecrutementDetailUsecase(
    IUseCase[GetRecrutementDetailQuery, RecrutementDetailReadModel | None]
):
    def __init__(
        self,
        organisme_permission_service: OrganismePermissionService,
        recrutement_query_service: IRecrutementQueryService,
    ):
        self.organisme_permission_service = organisme_permission_service
        self.recrutement_query_service = recrutement_query_service

    def execute(
        self, query: GetRecrutementDetailQuery
    ) -> RecrutementDetailReadModel | None:
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            recrutement_id=query.recrutement_id,
            utilisateur=query.utilisateur,
        )

        return self.recrutement_query_service.get_detail_by_recrutement(
            organisme_id=query.organisme_id, recrutement_id=query.recrutement_id
        )
