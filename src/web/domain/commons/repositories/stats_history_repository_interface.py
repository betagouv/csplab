from typing import Protocol

from domain.commons.entities.stats_history import StatsHistory


class IStatsHistoryRepository(Protocol):
    def save_stat(self, stats_history: StatsHistory) -> None: ...
