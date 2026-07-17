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
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement


@dataclass
class ListerMesRecrutementsQuery:
    organisme_id: UUID
    statut: StatutRecrutement


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
        logger: ILogger,
    ):
        self.logger = logger
        self.recrutement_query_service = recrutement_query_service
        self.organisme_repository = organisme_repository

    def execute(
        self, query: ListerMesRecrutementsQuery
    ) -> IPage[RecrutementActifsReadModel] | IPage[RecrutementArchivesReadModel]:
        self.logger.info(
            f"List mes recrutements pour l'organisme_id={query.organisme_id}",
        )

        # todo replace with rbac
        self.organisme_repository.get_by_id(query.organisme_id)

        if query.statut == StatutRecrutement.ACTIF:
            return self.recrutement_query_service.get_actifs_by_organisme(
                query.organisme_id
            )
        return self.recrutement_query_service.get_archives_by_organisme(
            query.organisme_id
        )
