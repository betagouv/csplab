from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class TalentsoftCredential:
    client_id: str
    client_secret: str
    base_url: str
    role: Literal["front", "back"]
