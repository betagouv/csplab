from dataclasses import dataclass
from typing import Optional


@dataclass
class GetFilteredMetiersInput:
    domain: Optional[str]
