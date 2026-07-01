from datetime import date

from domain.commons.services.offer_stats_query_service_interface import (
    IOfferStatsQueryService,
)
from domain.commons.services.stat_snapshot_writer_interface import IStatSnapshotWriter
from domain.commons.value_objects.stat_snapshot import StatSnapshot


class CalculateDailyStatsUseCase:
    def __init__(
        self,
        offer_stats_query_service: IOfferStatsQueryService,
        stat_snapshot_writer: IStatSnapshotWriter,
    ):
        self.offer_stats_query_service = offer_stats_query_service
        self.stat_snapshot_writer = stat_snapshot_writer

    def execute(self, target_date: date) -> None:
        snapshots = [
            StatSnapshot(
                date=target_date,
                metric_name="nb_published_offers",
                metric_value=self.offer_stats_query_service.count_published(),
            ),
            StatSnapshot(
                date=target_date,
                metric_name="nb_archived_offers",
                metric_value=self.offer_stats_query_service.count_archived(),
            ),
        ]
        for snapshot in snapshots:
            self.stat_snapshot_writer.write(snapshot)
