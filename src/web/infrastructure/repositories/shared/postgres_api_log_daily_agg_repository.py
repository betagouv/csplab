from datetime import date
from typing import List

from django.db import transaction
from referentiel.entities.api_log_daily_aggregation import ApiLogDailyAggregation
from referentiel.repositories.api_log_daily_aggregation_repository_interface import (
    IApiLogDailyAggregationRepository,
)

from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)


class PostgresApiLogDailyAggregationRepository(IApiLogDailyAggregationRepository):
    def replace_for_date(
        self, target_date: date, aggregations: List[ApiLogDailyAggregation]
    ) -> None:
        if not aggregations:
            raise ValueError(f"aggregations must not be empty for date {target_date}")
        with transaction.atomic():
            ApiLogDailyAggregationModel.objects.filter(date=target_date).delete()
            ApiLogDailyAggregationModel.objects.bulk_create(
                [ApiLogDailyAggregationModel.from_entity(agg) for agg in aggregations]
            )
