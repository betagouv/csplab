from dataclasses import dataclass
from uuid import UUID

from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase

from application.recruteur.services.recrutement_query_service_interface import (
    IRecrutementQueryService,
    RecrutementActifsReadModel,
    RecrutementArchivesReadModel,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement


@dataclass
class ListerMesRecrutementsQuery:
    organisme_id: UUID
    statut: StatutRecrutement
    utilisateur_id: UUID
    est_staff: bool = False


class ListerMesRecrutementsUsecase(
    IUseCase[
        ListerMesRecrutementsQuery,
        IPage[RecrutementActifsReadModel] | IPage[RecrutementArchivesReadModel],
    ]
):
    def __init__(
        self,
        recrutement_query_service: IRecrutementQueryService,
        organisme_repository: IOrganismeRepository,
        organisme_permission_service: OrganismePermissionService,
        logger: ILogger,
    ):
        self.logger = logger
        self.recrutement_query_service = recrutement_query_service
        self.organisme_repository = organisme_repository
        self.organisme_permission_service = organisme_permission_service

    def execute(
        self, query: ListerMesRecrutementsQuery
    ) -> IPage[RecrutementActifsReadModel] | IPage[RecrutementArchivesReadModel]:
        self.logger.info(
            f"List mes recrutements pour l'organisme_id={query.organisme_id}",
        )

        role = self.organisme_permission_service.est_autorise(
            action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
            organisme_id=query.organisme_id,
            agent_id=query.utilisateur_id,
            est_staff=query.est_staff,
        )
        self.organisme_repository.get_by_id(query.organisme_id)

        agent_id_filtre = (
            None if role == AgentOrganismeRole.RESPONSABLE else query.utilisateur_id
        )

        if query.statut == StatutRecrutement.ACTIF:
            return self.recrutement_query_service.get_actifs_by_organisme(
                query.organisme_id, agent_id_filtre
            )
        return self.recrutement_query_service.get_archives_by_organisme(
            query.organisme_id, agent_id_filtre
        )
