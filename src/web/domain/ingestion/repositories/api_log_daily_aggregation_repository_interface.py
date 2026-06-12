from datetime import date
from typing import List, Protocol

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation


class IApiLogDailyAggregationRepository(Protocol):
    def insert_for_date(
        self, target_date: date, aggregations: List[ApiLogDailyAggregation]
    ) -> None: ...
