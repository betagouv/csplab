from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

from domain.entities.offer import Offer
from domain.interfaces.page_interface import IPage


@dataclass
class GetFilteredOffersInput:
    active: bool
    external_id_contains: Optional[str]


class ListOffersResult(BaseModel):
    offers: List[Offer]

    class Config:
        arbitrary_types_allowed = True


class ListOffersQuerySetResult:
    def __init__(self, page: IPage[Offer]):
        self.page = page
