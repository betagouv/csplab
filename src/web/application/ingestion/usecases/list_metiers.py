from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.entities.metier import Metier
from referentiel.repositories.metier_repository_interface import IMetierRepository

from application.ingestion.interfaces.list_metiers_input import GetFilteredMetiersInput


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
