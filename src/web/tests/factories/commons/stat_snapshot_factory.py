from datetime import date

from domain.commons.value_objects.stat_snapshot import StatSnapshot
from infrastructure.django_apps.commons.models import StatSnapshotModel
from infrastructure.mappers.stat_snapshot_mapper import StatSnapshotMapper


class StatSnapshotFactory:
    _mapper = StatSnapshotMapper()

    @staticmethod
    def create_value_object(
        target_date: date = date(2026, 6, 30),
        metric_name: str = "nb_published_offers",
        metric_value: int = 0,
    ) -> StatSnapshot:
        return StatSnapshot(
            date=target_date,
            metric_name=metric_name,
            metric_value=metric_value,
        )

    @classmethod
    def create_model(
        cls,
        target_date: date = date(2026, 6, 30),
        metric_name: str = "nb_published_offers",
        metric_value: int = 0,
    ) -> StatSnapshotModel:
        snapshot = cls.create_value_object(
            target_date=target_date,
            metric_name=metric_name,
            metric_value=metric_value,
        )
        model = cls._mapper.from_domain(snapshot)
        model.save()
        return model
