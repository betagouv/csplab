from datetime import date

import pytest

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)

YESTERDAY = date(2026, 6, 9)
TODAY = date(2026, 6, 10)


def _agg(
    target_date: date,
    method: str = "GET",
    path: str = "/api/v1/offres/",
    token_type: str | None = None,
    count: int = 1,
) -> ApiLogDailyAggregation:
    return ApiLogDailyAggregation(
        date=target_date,
        method=method,
        path=path,
        token_type=token_type,
        count=count,
    )


@pytest.fixture
def repository():
    return SharedContainer().api_log_daily_aggregation_repository()


class TestInsertForDate:
    def test_persists_aggregations(self, db, repository):
        aggregations = [
            _agg(YESTERDAY, method="GET", path="/api/v1/offres/", count=5),
            _agg(YESTERDAY, method="POST", path="/api/v1/offres/", count=2),
        ]

        repository.insert_for_date(YESTERDAY, aggregations)

        rows = list(
            ApiLogDailyAggregationModel.objects.values(
                "date", "method", "path", "token_type", "count"
            )
        )
        assert {
            "date": YESTERDAY,
            "method": "GET",
            "path": "/api/v1/offres/",
            "token_type": None,
            "count": 5,
        } in rows
        assert {
            "date": YESTERDAY,
            "method": "POST",
            "path": "/api/v1/offres/",
            "token_type": None,
            "count": 2,
        } in rows

    def test_does_not_affect_other_dates(self, db, repository):
        repository.insert_for_date(TODAY, [_agg(TODAY, count=10)])
        repository.insert_for_date(YESTERDAY, [_agg(YESTERDAY, count=4)])

        assert ApiLogDailyAggregationModel.objects.filter(date=TODAY).count() == 1
        assert ApiLogDailyAggregationModel.objects.get(date=TODAY).count == 10  # noqa: PLR2004

    def test_raises_when_aggregations_empty(self, db, repository):
        with pytest.raises(ValueError):
            repository.insert_for_date(YESTERDAY, [])

    def test_persists_none_token_type(self, db, repository):
        repository.insert_for_date(
            YESTERDAY, [_agg(YESTERDAY, token_type=None, count=1)]
        )

        row = ApiLogDailyAggregationModel.objects.get(date=YESTERDAY)
        assert row.token_type is None
