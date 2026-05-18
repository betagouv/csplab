from dataclasses import dataclass
from typing import Optional

from domain.entities.offer import Offer
from domain.interfaces.page_interface import IPage


@dataclass
class GetFilteredOffersInput:
    active: bool
    external_id_contains: Optional[str]


class ListOffersPageResult:
    def __init__(self, page: IPage[Offer]):
        self.page = page
