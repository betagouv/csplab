from uuid import UUID

from application.ingestion.errors.application_errors_ingestion import (
    SourceIntrouvable,
)
from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.referentiel.models.offer import (
    OfferModel,
    OfferQuerySet,
)


def list_offers_by_source(source_id: UUID, search: str = "") -> OfferQuerySet:
    if not SourceModel.objects.filter(source_id=source_id).exists():
        raise SourceIntrouvable(source_id)
    return (
        OfferModel.objects.by_source(source_id)
        .actives()
        .search(search)
        .order_by("-updated_at", "pk")
    )
