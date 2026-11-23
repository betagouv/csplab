from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.django_apps.referentiel.models.offer_localisation import (
    OfferLocalisationModel,
)
from infrastructure.django_apps.utils.models import related_model


def test_related_model_returns_model_of_reverse_relation():
    assert related_model(OfferModel, "localisations") is OfferLocalisationModel


def test_related_model_returns_model_of_forward_relation():
    assert related_model(OfferLocalisationModel, "offer") is OfferModel
