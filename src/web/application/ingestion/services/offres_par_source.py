from uuid import UUID

from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.django_apps.referentiel.models.offer import (
    OfferModel,
    OfferQuerySet,
)
from infrastructure.django_apps.users.models import UserModel


def list_source_offers(source_id: UUID, user: UserModel | None) -> OfferQuerySet:
    if (
        user is not None
        and not user.is_superuser
        and not user.sources.filter(source_id=source_id).exists()
    ):
        raise SourceAuthorizationError({source_id})
    return (
        OfferModel.objects.by_source(source_id)
        .actives()
        .with_localisations()
        .order_by("-updated_at")
    )
