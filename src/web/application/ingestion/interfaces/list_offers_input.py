from dataclasses import dataclass
from typing import Optional


@dataclass
class GetFilteredOffersInput:
    active: bool
    external_id_contains: Optional[str]
