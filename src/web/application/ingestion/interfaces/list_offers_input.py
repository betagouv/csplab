from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel

from domain.entities.offer import Offer


@dataclass
class GetFilteredOffersInput:
    active: bool
    external_id_contains: Optional[str]


class ListOffersResult(BaseModel):
    offers: List[Offer]
