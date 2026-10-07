from uuid import UUID

from application.ingestion.errors.application_errors_ingestion import OffreIntrouvable
from application.ingestion.services.list_offers_by_source import list_offers_by_source
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.users.models import UserModel


def get_offer_by_source(user: UserModel, source_id: UUID, offer_id: UUID) -> OfferModel:
    offers = list_offers_by_source(user, source_id).select_related(
        "talentsoft_organisme_entity_code"
    )
    try:
        return offers.get(pk=offer_id)
    except OfferModel.DoesNotExist as e:
        raise OffreIntrouvable(offer_id) from e
