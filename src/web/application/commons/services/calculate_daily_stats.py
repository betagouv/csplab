from datetime import date

from infrastructure.django_apps.commons.enums import Metric
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel


def calculate_daily_stats(target_date: date) -> None:
    metrics = {
        Metric.PUBLISHED_OFFERS: OfferModel.objects.actives().count(),
        Metric.ARCHIVED_OFFERS: OfferModel.objects.archived().count(),
    }
    StatSnapshotModel.objects.bulk_create(
        [
            StatSnapshotModel(date=target_date, metric_name=name, metric_value=value)
            for name, value in metrics.items()
        ],
        update_conflicts=True,
        unique_fields=["date", "metric_name"],
        update_fields=["metric_value", "updated_at"],
    )
