from typing import Protocol

from domain.commons.value_objects.stat_snapshot import StatSnapshot


class IStatSnapshotWriter(Protocol):
    def write(self, snapshot: StatSnapshot) -> None: ...
