from datetime import UTC, date, datetime

from application.commons.services.calculate_daily_stats import calculate_daily_stats
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

TARGET_DATE = date(2026, 6, 30)


def snapshot_values(target_date: date) -> dict[str, int]:
    return dict(
        StatSnapshotModel.objects.filter(date=target_date).values_list(
            "metric_name", "metric_value"
        )
    )


def test_stores_offer_counts(db):
    OfferDjangoFactory.create_batch(3)
    OfferDjangoFactory.create_batch(2, archived_at=datetime.now(UTC))

    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values(TARGET_DATE) == {
        "nb_offres_publiees": 3,
        "nb_offres_archivees": 2,
    }


def test_stores_zero_without_offers(db):
    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values(TARGET_DATE) == {
        "nb_offres_publiees": 0,
        "nb_offres_archivees": 0,
    }


def test_rerun_for_same_date_replaces_values(db):
    calculate_daily_stats(TARGET_DATE)
    OfferDjangoFactory.create_batch(4)

    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values(TARGET_DATE) == {
        "nb_offres_publiees": 4,
        "nb_offres_archivees": 0,
    }


def test_keeps_snapshots_of_other_dates(db):
    other_date = date(2026, 6, 29)
    StatSnapshotModel.objects.create(
        date=other_date, metric_name="nb_offres_publiees", metric_value=7
    )

    calculate_daily_stats(TARGET_DATE)

    assert snapshot_values(other_date) == {"nb_offres_publiees": 7}
