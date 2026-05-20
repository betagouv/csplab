from dataclasses import dataclass
from typing import Optional

from domain.entities.metier import Metier
from domain.interfaces.page_interface import IPage


@dataclass
class GetFilteredMetiersInput:
    domain: Optional[str]


class ListMetiersPageResult:
    def __init__(self, page: IPage[Metier]):
        self.page = page
