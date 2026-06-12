from datetime import date
from typing import List

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation
from domain.ingestion.repositories import (
    api_log_daily_aggregation_repository_interface as agg_repo_interface,
)
from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)


class PostgresApiLogDailyAggregationRepository(
    agg_repo_interface.IApiLogDailyAggregationRepository
):
    def insert_for_date(
        self, target_date: date, aggregations: List[ApiLogDailyAggregation]
    ) -> None:
        if not aggregations:
            raise ValueError(f"aggregations must not be empty for date {target_date}")
        ApiLogDailyAggregationModel.objects.bulk_create(
            [ApiLogDailyAggregationModel.from_entity(agg) for agg in aggregations]
        )
