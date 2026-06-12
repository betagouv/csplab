from django.db import models

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation


class ApiLogDailyAggregationModel(models.Model):
    date = models.DateField()
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=2048)
    token_type = models.CharField(max_length=20, null=True, blank=True)
    count = models.PositiveIntegerField()

    def to_entity(self) -> ApiLogDailyAggregation:
        return ApiLogDailyAggregation(
            date=self.date,
            method=self.method,
            path=self.path,
            token_type=self.token_type,
            count=self.count,
        )

    @classmethod
    def from_entity(cls, agg: ApiLogDailyAggregation) -> "ApiLogDailyAggregationModel":
        return cls(
            date=agg.date,
            method=agg.method,
            path=agg.path,
            token_type=agg.token_type,
            count=agg.count,
        )

    class Meta:
        db_table = "api_logs_daily_aggregations"
        verbose_name = "API Log Daily Aggregation"
        verbose_name_plural = "API Log Daily Aggregations"
        constraints = [
            models.UniqueConstraint(
                fields=["date", "method", "path", "token_type"],
                name="api_logs_daily_agg_unique",
            )
        ]
        indexes = [
            models.Index(fields=["date"], name="api_logs_daily_agg_date_idx"),
        ]
