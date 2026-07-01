from domain.commons.services.offer_stats_query_service_interface import (
    IOfferStatsQueryService,
)
from infrastructure.django_apps.referentiel.models.offer import OfferModel


class PostgresOfferStatsQueryService(IOfferStatsQueryService):
    def count_published(self) -> int:
        return OfferModel.objects.filter(archived_at__isnull=True).count()

    def count_archived(self) -> int:
        return OfferModel.objects.filter(archived_at__isnull=False).count()
