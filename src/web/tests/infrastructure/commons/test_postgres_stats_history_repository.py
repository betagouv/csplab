from datetime import date

import pytest
from django.db import IntegrityError

from domain.commons.entities.stats_history import StatsHistory
from infrastructure.django_apps.commons.models import StatsHistoryModel
from infrastructure.repositories.commons.postgres_stats_history_repository import (
    PostgresStatsHistoryRepository,
)
from tests.factories.commons.stats_history_factory import StatsHistoryFactory

TODAY = date(2026, 6, 30)
YESTERDAY = date(2026, 6, 29)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresStatsHistoryRepository()


class TestSaveStat:
    def test_creates_new_row(self, db, repository):
        stat = StatsHistoryFactory.create_entity(
            target_date=TODAY, metric_name="nb_published_offers", metric_value=100
        )

        repository.save_stat(stat)

        saved = StatsHistoryModel.objects.get(
            date=TODAY, metric_name="nb_published_offers"
        )
        assert saved.metric_value == 100  # noqa: PLR2004

    def test_raises_on_duplicate(self, db, repository):
        StatsHistoryFactory.create_model(
            target_date=TODAY, metric_name="nb_published_offers", metric_value=100
        )

        with pytest.raises(IntegrityError):
            repository.save_stat(
                StatsHistory(
                    date=TODAY, metric_name="nb_published_offers", metric_value=150
                )
            )

    def test_different_metrics_on_same_date_are_independent(self, db, repository):
        repository.save_stat(
            StatsHistoryFactory.create_entity(
                target_date=TODAY,
                metric_name="nb_published_offers",
                metric_value=10,
            )
        )
        repository.save_stat(
            StatsHistoryFactory.create_entity(
                target_date=TODAY,
                metric_name="nb_archived_offers",
                metric_value=5,
            )
        )

        assert StatsHistoryModel.objects.count() == 2  # noqa: PLR2004

    def test_same_metric_on_different_dates_are_independent(self, db, repository):
        repository.save_stat(
            StatsHistoryFactory.create_entity(
                target_date=TODAY, metric_name="nb_published_offers", metric_value=10
            )
        )
        repository.save_stat(
            StatsHistoryFactory.create_entity(
                target_date=YESTERDAY,
                metric_name="nb_published_offers",
                metric_value=8,
            )
        )

        assert StatsHistoryModel.objects.count() == 2  # noqa: PLR2004
        assert (
            StatsHistoryModel.objects.get(
                date=TODAY, metric_name="nb_published_offers"
            ).metric_value
            == 10  # noqa: PLR2004
        )
        assert (
            StatsHistoryModel.objects.get(
                date=YESTERDAY, metric_name="nb_published_offers"
            ).metric_value
            == 8  # noqa: PLR2004
        )
