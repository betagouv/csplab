from domain.commons.services.stat_snapshot_writer_interface import IStatSnapshotWriter
from domain.commons.value_objects.stat_snapshot import StatSnapshot
from infrastructure.mappers.stat_snapshot_mapper import StatSnapshotMapper


class PostgresStatSnapshotWriter(IStatSnapshotWriter):
    def __init__(self) -> None:
        self.mapper = StatSnapshotMapper()

    def write(self, snapshot: StatSnapshot) -> None:
        self.mapper.from_domain(snapshot).save()
