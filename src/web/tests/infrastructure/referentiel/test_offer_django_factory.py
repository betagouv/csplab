from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_build_accepts_the_main_localisation_kwargs():
    offer = OfferDjangoFactory.build(department="69", location_label="Lyon")

    assert offer.pk is not None
    assert offer._state.adding
