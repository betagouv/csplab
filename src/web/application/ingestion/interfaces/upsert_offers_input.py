from dataclasses import dataclass

from domain.entities.offer import Offer


@dataclass
class UpsertOffersInput:
    offers: list[Offer]
