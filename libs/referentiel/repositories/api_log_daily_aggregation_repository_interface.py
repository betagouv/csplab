from datetime import date
from typing import List, Protocol

from referentiel.entities.api_log_daily_aggregation import ApiLogDailyAggregation


class IApiLogDailyAggregationRepository(Protocol):
    def replace_for_date(
        self, target_date: date, aggregations: List[ApiLogDailyAggregation]
    ) -> None: ...
