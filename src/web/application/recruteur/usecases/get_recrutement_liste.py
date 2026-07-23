from dataclasses import dataclass
from uuid import UUID

from ddd.usecase_interface import IUseCase

from application.recruteur.dtos.recrutement_read_models import (
    CandidatureListeReadModel,
)
from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class GetRecrutementListeQuery:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False


class GetRecrutementListeUsecase(
    IUseCase[GetRecrutementListeQuery, list[CandidatureListeReadModel] | None]
):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        organisme_permission_service: OrganismePermissionService,
        recrutement_query_service: IRecrutementQueryService,
    ):
        self.organisme_repository = organisme_repository
        self.organisme_permission_service = organisme_permission_service
        self.recrutement_query_service = recrutement_query_service

    def execute(
        self, query: GetRecrutementListeQuery
    ) -> list[CandidatureListeReadModel] | None:
        # TODO RBAC : handle MEMBRE role on recrutement
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            agent_id=query.utilisateur_id,
            est_staff=query.est_staff,
        )
        self.organisme_repository.get_by_id(query.organisme_id)

        return self.recrutement_query_service.get_candidatures_by_recrutement(
            organisme_id=query.organisme_id, recrutement_id=query.recrutement_id
        )
