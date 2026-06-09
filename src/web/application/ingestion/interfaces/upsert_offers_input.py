from dataclasses import dataclass

from referentiel.entities.offer import Offer


@dataclass
class UpsertOffersInput:
    offers: list[Offer]
