from dataclasses import dataclass

from domain.entities.offer import Offer
from domain.repositories.document_repository_interface import IUpsertResult


@dataclass
class UpsertOffersInput:
    offers: list[Offer]


UpsertOffersResult = IUpsertResult
