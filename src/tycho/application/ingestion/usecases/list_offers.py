from dataclasses import dataclass
from datetime import datetime

from domain.entities.offer import Offer
from domain.interfaces.usecase_interface import IUseCase
from domain.repositories.offers_repository_interface import IOffersRepository


@dataclass
class GetOffersCommand:
    active: bool
    after: datetime
    before: datetime


@dataclass
class ListOffersResult:
    offers: list[Offer]


class ListOffersUseCase(IUseCase[GetOffersCommand, ListOffersResult]):
    def __init__(self, offers_repository: IOffersRepository):
        self.offers_repository = offers_repository

    def execute(self, input_data: GetOffersCommand) -> ListOffersResult:
        offers = self.offers_repository.get_by_status_and_period(
            active=input_data.active,
            after=input_data.after,
            before=input_data.before,
        )
        return ListOffersResult(offers=offers)
