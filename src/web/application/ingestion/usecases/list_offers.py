from application.ingestion.interfaces.list_offers_input import (
    GetFilteredOffersInput,
    ListOffersPageResult,
)
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import IOffersRepository
from domain.services.logger_interface import ILogger


class ListOffersUseCase(IUseCase[GetFilteredOffersInput, ListOffersPageResult]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        logger: ILogger,
    ):
        self.offers_repository = offers_repository
        self.logger = logger

    def execute(self, input_data: GetFilteredOffersInput) -> ListOffersPageResult:
        page = self.offers_repository.get_filtered(
            active=input_data.active,
            external_id_contains=input_data.external_id_contains,
        )
        return ListOffersPageResult(page=page)
