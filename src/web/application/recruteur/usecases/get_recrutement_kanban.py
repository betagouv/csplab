from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ddd.usecase_interface import IUseCase

from application.recruteur.usecases.recrutement_detail_static_data import (
    STATIC_RECRUTEMENTS_DETAIL_BY_ID,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction


@dataclass
class GetRecrutementKanbanQuery:
    organisme_id: UUID
    recrutement_id: UUID
    utilisateur_id: UUID
    est_staff: bool = False


class GetRecrutementKanbanUsecase(
    IUseCase[GetRecrutementKanbanQuery, dict[str, Any] | None]
):
    def __init__(
        self,
        organisme_repository: IOrganismeRepository,
        organisme_permission_service: OrganismePermissionService,
    ):
        self.organisme_repository = organisme_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(self, query: GetRecrutementKanbanQuery) -> dict[str, Any] | None:
        # TODO RBAC : handle MEMBRE role on recrutement
        self.organisme_permission_service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=query.organisme_id,
            agent_id=query.utilisateur_id,
            est_staff=query.est_staff,
        )
        self.organisme_repository.get_by_id(query.organisme_id)

        return STATIC_RECRUTEMENTS_DETAIL_BY_ID.get(str(query.recrutement_id))
