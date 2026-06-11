from datetime import date

import pytest

from infrastructure.django_apps.ingestion.models.api_log_daily_aggregation import (
    ApiLogDailyAggregationModel,
)
from presentation.ingestion.tasks import aggregate_api_logs
from tests.factories.datetime_utils import date_to_aware_datetime
from tests.factories.ingestion.api_log_model_factory import ApiLogModelFactory

TODAY = date(2026, 6, 10)
YESTERDAY = date(2026, 6, 9)


def _rows() -> list[dict]:
    return list(
        ApiLogDailyAggregationModel.objects.values(
            "date", "method", "path", "token_type", "count"
        )
    )


def _row(method: str, path: str, token_type: str | None, count: int) -> dict:
    return {
        "date": YESTERDAY,
        "method": method,
        "path": path,
        "token_type": token_type,
        "count": count,
    }


@pytest.fixture(autouse=True)
def clean_aggregations(db):
    ApiLogDailyAggregationModel.objects.all().delete()


class TestAggregateApiLogsTask:
    def test_produces_correct_row(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)

        assert _rows() == [_row("GET", "/api/v1/offres/", "jwt", 2)]

    def test_creates_one_row_per_combination(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="POST",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/metiers/",
            method="GET",
            token_type="api_key",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)

        rows = _rows()
        assert _row("GET", "/api/v1/offres/", "jwt", 1) in rows
        assert _row("POST", "/api/v1/offres/", "jwt", 1) in rows
        assert _row("GET", "/api/v1/metiers/", "api_key", 1) in rows

    def test_groups_by_token_type(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="api_key",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)

        rows = _rows()
        assert _row("GET", "/api/v1/offres/", "jwt", 1) in rows
        assert _row("GET", "/api/v1/offres/", "api_key", 1) in rows
        assert _row("GET", "/api/v1/offres/", None, 1) in rows

    def test_ignores_other_dates(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(TODAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)

        assert _rows() == [_row("GET", "/api/v1/offres/", "jwt", 1)]

    def test_is_idempotent(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)
        aggregate_api_logs.call_local(target_date=YESTERDAY)

        assert _rows() == [_row("GET", "/api/v1/offres/", "jwt", 1)]

    def test_produces_no_rows_when_no_logs(self, db):
        aggregate_api_logs.call_local(target_date=YESTERDAY)

        assert _rows() == []

    def test_groups_by_path(self, db):
        ApiLogModelFactory.create_model(
            path="/api/v1/offres/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            path="/api/v1/metiers/",
            method="GET",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        aggregate_api_logs.call_local(target_date=YESTERDAY)

        rows = _rows()
        assert _row("GET", "/api/v1/offres/", "jwt", 1) in rows
        assert _row("GET", "/api/v1/metiers/", "jwt", 1) in rows
