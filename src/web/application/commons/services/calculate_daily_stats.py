from datetime import date

from django.db import transaction

from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel


def calculate_daily_stats(target_date: date) -> None:
    metrics = {
        "nb_published_offers": OfferModel.objects.actives().count(),
        "nb_archived_offers": OfferModel.objects.archived().count(),
    }
    with transaction.atomic():
        StatSnapshotModel.objects.bulk_create(
            [
                StatSnapshotModel(
                    date=target_date, metric_name=name, metric_value=value
                )
                for name, value in metrics.items()
            ],
            update_conflicts=True,
            unique_fields=["date", "metric_name"],
            update_fields=["metric_value", "updated_at"],
        )
