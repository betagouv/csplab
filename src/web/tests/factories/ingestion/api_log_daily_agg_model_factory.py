from datetime import date
from typing import Optional, TypedDict

from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)


class ApiLogDailyAggregationRow(TypedDict):
    date: date
    method: str
    path: str
    token_type: str | None
    count: int


class ApiLogDailyAggregationModelFactory:
    @staticmethod
    def create_model(
        target_date: date = date(2026, 6, 10),
        method: str = "GET",
        path: str = "/api/v1/offres/",
        token_type: Optional[str] = None,
        count: int = 1,
    ) -> ApiLogDailyAggregationModel:
        model = ApiLogDailyAggregationModel(
            date=target_date,
            method=method,
            path=path,
            token_type=token_type,
            count=count,
        )
        model.save()
        return model

    @staticmethod
    def all_as_dicts() -> list[ApiLogDailyAggregationRow]:
        return [
            {
                "date": m.date,
                "method": m.method,
                "path": m.path,
                "token_type": m.token_type,
                "count": m.count,
            }
            for m in ApiLogDailyAggregationModel.objects.all()
        ]

    @staticmethod
    def count_for_date(target_date: date) -> int:
        return ApiLogDailyAggregationModel.objects.filter(date=target_date).count()

    @staticmethod
    def get_for_date(target_date: date) -> ApiLogDailyAggregationModel:
        return ApiLogDailyAggregationModel.objects.get(date=target_date)
