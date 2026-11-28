from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.django_apps.referentiel.models.offer import (
    OfferModel,
    OfferQuerySet,
)


def list_offers(filters: GetFilteredOffersInput) -> OfferQuerySet:
    return OfferModel.objects.filtered(**vars(filters))
