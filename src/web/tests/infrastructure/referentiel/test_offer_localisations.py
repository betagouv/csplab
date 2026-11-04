import pytest

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

CAEN = {"area": "EU", "country": "FRA", "region": "28", "department": "14"}
LYON = {
    "area": "EU",
    "country": "FRA",
    "region": "84",
    "department": "69",
    "latitude": 45.7640,
    "longitude": 4.8357,
}
BERLIN = {"area": "EU", "country": "DEU", "label": "Berlin"}

pytestmark = pytest.mark.django_db


def _ids(queryset) -> set:
    return set(queryset.values_list("id", flat=True))


class TestWithLocalisationIn:
    def test_matches_any_localisation_of_the_offer(self):
        caen_and_lyon = OfferDjangoFactory(localisations=[CAEN, LYON])
        OfferDjangoFactory(localisations=[CAEN])

        assert _ids(OfferModel.objects.with_localisation_in(departments=["69"])) == {
            caen_and_lyon.id
        }

    def test_every_filter_applies_to_the_same_localisation(self):
        OfferDjangoFactory(localisations=[CAEN, LYON])

        offers = OfferModel.objects.with_localisation_in(
            regions=["28"], departments=["69"]
        )

        assert not offers.exists()

    def test_returns_each_offer_once(self):
        OfferDjangoFactory(localisations=[CAEN, {**CAEN, "label": "Bayeux"}])

        assert OfferModel.objects.with_localisation_in(departments=["14"]).count() == 1

    def test_without_filter_keeps_every_offer(self):
        OfferDjangoFactory(localisations=[])

        assert OfferModel.objects.with_localisation_in().count() == 1


class TestWithLocalisationWithin:
    def test_matches_an_offer_with_one_localisation_in_the_radius(self):
        caen_and_lyon = OfferDjangoFactory(localisations=[CAEN, LYON])
        OfferDjangoFactory(localisations=[CAEN])

        offers = OfferModel.objects.with_localisation_within(45.76, 4.84, 10)

        assert _ids(offers) == {caen_and_lyon.id}
