from datetime import date

from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from presentation.ingestion.tasks import calculate_daily_stats

TARGET_DATE = date(2026, 6, 30)


def test_task_stores_daily_snapshots(db):
    OfferDjangoFactory()

    calculate_daily_stats.call_local(target_date=TARGET_DATE)

    assert (
        StatSnapshotModel.objects.get(
            date=TARGET_DATE, metric_name="nb_published_offers"
        ).metric_value
        == 1
    )
