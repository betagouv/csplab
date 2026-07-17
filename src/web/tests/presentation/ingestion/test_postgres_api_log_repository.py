from datetime import date

import pytest

from domain.ingestion.entities.api_log_daily_aggregation import ApiLogDailyAggregation
from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel
from infrastructure.factories.api_log_factory import ApiLogFactory
from infrastructure.factories.datetime_utils import date_to_aware_datetime
from infrastructure.factories.ingestion.api_log_model_factory import ApiLogModelFactory

TODAY = date(2026, 6, 10)
YESTERDAY = date(2026, 6, 9)


@pytest.fixture
def repository():
    return SharedContainer().api_log_repository()


class TestSave:
    def test_persists_api_log(self, db, repository):
        api_log = ApiLogFactory.create_entity()

        repository.save(api_log)

        saved = ApiLogModel.objects.get()
        assert saved.to_entity() == api_log

    def test_multiple_logs_are_independent(self, db, repository):
        log_a = ApiLogFactory.create_entity(path="/api/v1/offres/")
        log_b = ApiLogFactory.create_entity(path="/api/v1/sources/")

        repository.save(log_a)
        repository.save(log_b)

        assert ApiLogModel.objects.count() == 2  # noqa: PLR2004


class TestGetCountsByDate:
    def test_returns_empty_list_when_no_logs(self, db, repository):
        assert repository.get_counts_by_date(YESTERDAY) == []

    def test_returns_correct_aggregation(self, db, repository):
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

        result = repository.get_counts_by_date(YESTERDAY)

        assert result == [
            ApiLogDailyAggregation(
                date=YESTERDAY,
                method="GET",
                path="/api/v1/offres/",
                token_type="jwt",  # noqa: S106
                count=2,
            )
        ]

    def test_groups_by_method(self, db, repository):
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            method="POST",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        result = repository.get_counts_by_date(YESTERDAY)

        methods = {r.method for r in result}
        assert methods == {"GET", "POST"}
        for row in result:
            assert row.count == 1

    def test_groups_by_path(self, db, repository):
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/metiers/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        result = repository.get_counts_by_date(YESTERDAY)

        paths = {r.path for r in result}
        assert paths == {"/api/v1/offres/", "/api/v1/metiers/"}

    def test_groups_by_token_type(self, db, repository):
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type="jwt",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type="api_key",  # noqa: S106
            timestamp=date_to_aware_datetime(YESTERDAY),
        )
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        result = repository.get_counts_by_date(YESTERDAY)

        token_types = {r.token_type for r in result}
        assert token_types == {"jwt", "api_key", None}

    def test_ignores_other_dates(self, db, repository):
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(TODAY),
        )
        ApiLogModelFactory.create_model(
            method="GET",
            path="/api/v1/offres/",
            token_type=None,
            timestamp=date_to_aware_datetime(YESTERDAY),
        )

        result = repository.get_counts_by_date(YESTERDAY)

        assert len(result) == 1
        assert result[0].date == YESTERDAY


class TestDeleteBefore:
    def test_deletes_rows_older_than_cutoff(self, db, repository):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(YESTERDAY))

        deleted = repository.delete_before(TODAY)

        assert deleted == 1
        assert ApiLogModel.objects.count() == 0

    def test_keeps_rows_on_cutoff_date(self, db, repository):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(TODAY))

        deleted = repository.delete_before(TODAY)

        assert deleted == 0
        assert ApiLogModel.objects.count() == 1

    def test_keeps_rows_after_cutoff_date(self, db, repository):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(TODAY))

        deleted = repository.delete_before(YESTERDAY)

        assert deleted == 0
        assert ApiLogModel.objects.count() == 1

    def test_returns_zero_when_nothing_to_delete(self, db, repository):
        deleted = repository.delete_before(TODAY)

        assert deleted == 0

    def test_deletes_only_old_rows(self, db, repository):
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(YESTERDAY))
        ApiLogModelFactory.create_model(timestamp=date_to_aware_datetime(TODAY))

        deleted = repository.delete_before(TODAY)

        assert deleted == 1
        assert ApiLogModel.objects.count() == 1
