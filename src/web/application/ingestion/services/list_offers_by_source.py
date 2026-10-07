from uuid import UUID

from application.ingestion.errors.application_errors_ingestion import (
    SourceNonAutorisee,
)
from application.ingestion.services.list_authorized_sources import (
    list_authorized_sources,
)
from infrastructure.django_apps.referentiel.models.offer import (
    OfferModel,
    OfferQuerySet,
)
from infrastructure.django_apps.users.models import UserModel


def list_offers_by_source(
    user: UserModel, source_id: UUID, search: str = ""
) -> OfferQuerySet:
    sources = list_authorized_sources(user)
    if not sources.filter(source_id=source_id).exists():
        raise SourceNonAutorisee(source_id)
    return (
        OfferModel.objects.by_source(source_id)
        .actives()
        .search(search)
        .order_by("-updated_at", "pk")
    )
