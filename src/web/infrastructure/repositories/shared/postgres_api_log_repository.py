from datetime import date
from typing import List

from django.db.models import Count
from referentiel.entities.api_log import ApiLog

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation
from domain.ingestion.repositories.api_log_repository_interface import IApiLogRepository
from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel


class PostgresApiLogRepository(IApiLogRepository):
    def save(self, api_log: ApiLog) -> None:
        ApiLogModel.from_entity(api_log).save()

    def delete_before(self, cutoff: date) -> int:
        deleted, _ = ApiLogModel.objects.filter(timestamp__date__lt=cutoff).delete()
        return deleted

    def get_counts_by_date(self, target_date: date) -> List[ApiLogDailyAggregation]:
        rows = (
            ApiLogModel.objects.filter(timestamp__date=target_date)
            .values("method", "path", "token_type")
            .annotate(count=Count("id"))
        )
        return [
            ApiLogDailyAggregation(
                date=target_date,
                method=row["method"],
                path=row["path"],
                token_type=row["token_type"],
                count=row["count"],
            )
            for row in rows
        ]
