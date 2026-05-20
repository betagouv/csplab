from application.ingestion.interfaces.list_metiers_input import (
    GetFilteredMetiersInput,
    ListMetiersPageResult,
)
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.services.logger_interface import ILogger


class ListMetiersUseCase(IUseCase[GetFilteredMetiersInput, ListMetiersPageResult]):
    def __init__(
        self,
        metiers_repository: IMetierRepository,
        logger: ILogger,
    ):
        self.metiers_repository = metiers_repository
        self.logger = logger

    def execute(self, input_data: GetFilteredMetiersInput) -> ListMetiersPageResult:
        predicate = (
            {"domaine_fonctionnel_code": input_data.domain} if input_data.domain else {}
        )
        page = self.metiers_repository.get_filtered_slice(predicate)
        return ListMetiersPageResult(page=page)
