from typing import Protocol

from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer


class IOffersCleaner(Protocol):
    def clean(self, raw_offer: RawOffer) -> Offer: ...
