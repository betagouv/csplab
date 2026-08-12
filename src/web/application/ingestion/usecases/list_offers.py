from ddd.page_interface import IPage
from ddd.services.logger_interface import ILogger
from ddd.usecase_interface import IUseCase
from referentiel.entities.offer import Offer
from referentiel.repositories.offers_repository_interface import IOffersRepository

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput


class ListOffersUseCase(IUseCase[GetFilteredOffersInput, IPage[Offer]]):
    def __init__(
        self,
        offers_repository: IOffersRepository,
        logger: ILogger,
    ):
        self.offers_repository = offers_repository
        self.logger = logger

    def execute(self, input_data: GetFilteredOffersInput) -> IPage[Offer]:
        return self.offers_repository.get_filtered(
            active=input_data.active,
            external_id_contains=input_data.external_id_contains,
            category=input_data.category,
            verse=input_data.verse,
            contract_type=input_data.contract_type,
            experience_level=input_data.experience_level,
            management=input_data.management,
            working_place=input_data.working_place,
            region=input_data.region,
            department=input_data.department,
            country=input_data.country,
            area=input_data.area,
            domain=input_data.domain,
            organization=input_data.organization,
            published_within_days=input_data.published_within_days,
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            radius_km=input_data.radius_km,
            keywords=input_data.keywords,
        )
