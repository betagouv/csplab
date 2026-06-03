from ddd.page_interface import IPage
from ddd.usecase_interface import IUseCase

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput
from domain.entities.metier import Metier
from domain.repositories.metier_repository_interface import IMetierRepository
from domain.services.logger_interface import ILogger


class ListMetiersUseCase(IUseCase[GetFilteredMetiersInput, IPage[Metier]]):
    def __init__(
        self,
        metiers_repository: IMetierRepository,
        logger: ILogger,
    ):
        self.metiers_repository = metiers_repository
        self.logger = logger

    def execute(self, input_data: GetFilteredMetiersInput) -> IPage[Metier]:
        predicate = (
            {"domaine_fonctionnel_code": input_data.domain} if input_data.domain else {}
        )
        return self.metiers_repository.get_filtered_slice(predicate)
