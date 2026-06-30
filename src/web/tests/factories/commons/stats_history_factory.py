from datetime import date

from domain.commons.entities.stats_history import StatsHistory
from infrastructure.django_apps.commons.models import StatsHistoryModel


class StatsHistoryFactory:
    @staticmethod
    def create_entity(
        target_date: date = date(2026, 6, 30),
        metric_name: str = "nb_published_offers",
        metric_value: int = 0,
    ) -> StatsHistory:
        return StatsHistory(
            date=target_date,
            metric_name=metric_name,
            metric_value=metric_value,
        )

    @staticmethod
    def create_model(
        target_date: date = date(2026, 6, 30),
        metric_name: str = "nb_published_offers",
        metric_value: int = 0,
    ) -> StatsHistoryModel:
        entity = StatsHistoryFactory.create_entity(
            target_date=target_date,
            metric_name=metric_name,
            metric_value=metric_value,
        )
        model = StatsHistoryModel.from_entity(entity)
        model.save()
        return model
