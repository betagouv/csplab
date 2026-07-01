from domain.commons.entities.stats_history import StatsHistory
from domain.commons.repositories.stats_history_repository_interface import (
    IStatsHistoryRepository,
)
from infrastructure.django_apps.commons.models import StatsHistoryModel


class PostgresStatsHistoryRepository(IStatsHistoryRepository):
    def save(self, stats_history: StatsHistory) -> None:
        StatsHistoryModel.from_entity(stats_history).save()
