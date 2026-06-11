from datetime import date
from typing import List, Protocol

from referentiel.entities.api_log import ApiLog
from referentiel.entities.api_log_daily_aggregation import ApiLogDailyAggregation


class IApiLogRepository(Protocol):
    def save(self, api_log: ApiLog) -> None: ...

    def get_counts_by_date(self, target_date: date) -> List[ApiLogDailyAggregation]: ...

    def delete_before(self, cutoff: date) -> int: ...
