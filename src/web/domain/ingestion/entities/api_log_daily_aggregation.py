from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class ApiLogDailyAggregation:
    date: date
    method: str
    path: str
    token_type: Optional[str]
    count: int
