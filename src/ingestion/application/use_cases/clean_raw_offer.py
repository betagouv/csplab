from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer
from domain.gateways.offers_cleaner import IOffersCleaner


class CleanRawOfferUseCase:
    def __init__(self, offers_cleaner: IOffersCleaner) -> None:
        self._offers_cleaner = offers_cleaner

    def execute(self, raw_offer: RawOffer) -> Offer:
        return self._offers_cleaner.clean(raw_offer)
