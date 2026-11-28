from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from application.ingestion.services.liste_offres import list_offers
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_lists_the_offers_matching_the_filters(db):
    offer = OfferDjangoFactory(verse=Verse.FPT.value)
    OfferDjangoFactory(verse=Verse.FPE.value)

    offers = list_offers(GetFilteredOffersInput(active=True, verse=[Verse.FPT]))

    assert list(offers) == [offer]
