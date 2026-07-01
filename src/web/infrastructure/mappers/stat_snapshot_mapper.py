from ddd.mapper_interface import IFromDomainMapper, IToDomainMapper

from domain.commons.value_objects.stat_snapshot import StatSnapshot
from infrastructure.django_apps.commons.models import StatSnapshotModel


class StatSnapshotMapper(IFromDomainMapper, IToDomainMapper):
    def from_domain(self, snapshot: StatSnapshot) -> StatSnapshotModel:
        return StatSnapshotModel(
            date=snapshot.date,
            metric_name=snapshot.metric_name,
            metric_value=snapshot.metric_value,
        )

    def to_domain(self, model: StatSnapshotModel) -> StatSnapshot:
        return StatSnapshot(
            date=model.date,
            metric_name=model.metric_name,
            metric_value=model.metric_value,
        )
