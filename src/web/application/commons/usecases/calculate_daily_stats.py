from datetime import date

from domain.commons.entities.stats_history import StatsHistory
from domain.commons.repositories.stats_history_repository_interface import (
    IStatsHistoryRepository,
)
from domain.ingestion.repositories.ingestion_offers_repository_interface import (
    IIngestionOffersRepository,
)


class CalculateDailyStatsUseCase:
    def __init__(
        self,
        offers_repository: IIngestionOffersRepository,
        stats_history_repository: IStatsHistoryRepository,
    ):
        self.offers_repository = offers_repository
        self.stats_history_repository = stats_history_repository

    def execute(self, target_date: date) -> None:
        stats = [
            StatsHistory(
                date=target_date,
                metric_name="nb_published_offers",
                metric_value=self.offers_repository.count_published(),
            ),
            StatsHistory(
                date=target_date,
                metric_name="nb_archived_offers",
                metric_value=self.offers_repository.count_archived(),
            ),
        ]
        for stat in stats:
            self.stats_history_repository.save_stat(stat)
