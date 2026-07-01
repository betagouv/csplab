from datetime import date
from unittest.mock import MagicMock

import pytest

from domain.commons.value_objects.stat_snapshot import StatSnapshot

TARGET_DATE = date(2026, 6, 30)


class TestCalculateDailyStats:
    def setup_mocks(self, usecase, *, published_count=0, archived_count=0):
        usecase.offer_stats_query_service.count_published = MagicMock(
            return_value=published_count
        )
        usecase.offer_stats_query_service.count_archived = MagicMock(
            return_value=archived_count
        )
        usecase.stat_snapshot_writer.write = MagicMock()

    def test_stores_published_offers_count(self, calculate_daily_stats_usecase):
        self.setup_mocks(calculate_daily_stats_usecase, published_count=3)

        calculate_daily_stats_usecase.execute(TARGET_DATE)

        calculate_daily_stats_usecase.stat_snapshot_writer.write.assert_any_call(
            StatSnapshot(
                date=TARGET_DATE, metric_name="nb_published_offers", metric_value=3
            )
        )

    def test_stores_archived_offers_count(self, calculate_daily_stats_usecase):
        self.setup_mocks(calculate_daily_stats_usecase, archived_count=2)

        calculate_daily_stats_usecase.execute(TARGET_DATE)

        calculate_daily_stats_usecase.stat_snapshot_writer.write.assert_any_call(
            StatSnapshot(
                date=TARGET_DATE, metric_name="nb_archived_offers", metric_value=2
            )
        )

    def test_stores_both_metrics(self, calculate_daily_stats_usecase):
        self.setup_mocks(
            calculate_daily_stats_usecase, published_count=4, archived_count=1
        )

        calculate_daily_stats_usecase.execute(TARGET_DATE)

        write = calculate_daily_stats_usecase.stat_snapshot_writer.write
        assert write.call_count == 2  # noqa: PLR2004

    def test_propagates_write_error(self, calculate_daily_stats_usecase):
        self.setup_mocks(calculate_daily_stats_usecase, published_count=5)
        calculate_daily_stats_usecase.stat_snapshot_writer.write = MagicMock(
            side_effect=Exception("db error")
        )

        with pytest.raises(Exception, match="db error"):
            calculate_daily_stats_usecase.execute(TARGET_DATE)
