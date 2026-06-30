from datetime import date, datetime

import pytest
from django.db import IntegrityError

from infrastructure.django_apps.commons.models import StatsHistoryModel
from tests.factories.referentiel.offer_factory import OfferFactory

TARGET_DATE = date(2026, 6, 30)


class TestCalculateDailyStats:
    def test_stores_published_offers_count(self, db, ingestion_container):
        OfferFactory.create_model_batch(3)

        ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)

        stat = StatsHistoryModel.objects.get(
            date=TARGET_DATE, metric_name="nb_published_offers"
        )
        assert stat.metric_value == 3  # noqa: PLR2004

    def test_stores_archived_offers_count(self, db, ingestion_container):
        OfferFactory.create_model_batch(2, archived_at=datetime.now())

        ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)

        stat = StatsHistoryModel.objects.get(
            date=TARGET_DATE, metric_name="nb_archived_offers"
        )
        assert stat.metric_value == 2  # noqa: PLR2004

    def test_stores_both_metrics(self, db, ingestion_container):
        OfferFactory.create_model_batch(4)
        OfferFactory.create_model_batch(1, archived_at=datetime.now())

        ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)

        assert StatsHistoryModel.objects.filter(date=TARGET_DATE).count() == 2  # noqa: PLR2004

    def test_raises_on_duplicate_date(self, db, ingestion_container):
        OfferFactory.create_model_batch(5)

        ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)

        with pytest.raises(IntegrityError):
            ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)
