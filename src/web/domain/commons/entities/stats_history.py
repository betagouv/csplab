from dataclasses import dataclass
from datetime import date


@dataclass
class StatsHistory:
    date: date
    metric_name: str
    metric_value: int
