from datetime import date, datetime

from infrastructure.django_apps.commons.models import StatSnapshotModel
from tests.factories.referentiel.offer_factory import OfferFactory

TARGET_DATE = date(2026, 6, 30)

PUBLISHED = 3
ARCHIVED = 2


class TestCalculateDailyStats:
    def test_stores_stats_snapshots_in_database(self, ingestion_container):
        OfferFactory.create_model_batch(PUBLISHED)
        OfferFactory.create_model_batch(ARCHIVED, archived_at=datetime.now())

        ingestion_container.calculate_daily_stats_usecase().execute(TARGET_DATE)

        published_snapshot = StatSnapshotModel.objects.get(
            date=TARGET_DATE, metric_name="nb_published_offers"
        )
        assert published_snapshot.metric_value == PUBLISHED

        archived_snapshot = StatSnapshotModel.objects.get(
            date=TARGET_DATE, metric_name="nb_archived_offers"
        )
        assert archived_snapshot.metric_value == ARCHIVED
