from django.utils import timezone

from application.ingestion.services.metier_functional_areas import (
    get_metier_functional_areas,
)
from infrastructure.factories.referentiel.metier_django_factory import (
    MetierDjangoFactory,
)


def test_returns_the_metier_functional_area(db):
    MetierDjangoFactory(offer_family_code="ERACH001", domaine_fonctionnel_code="ACH")
    MetierDjangoFactory(offer_family_code="ERNUM001", domaine_fonctionnel_code="NUM")

    assert get_metier_functional_areas("ERACH001") == {"ACH"}


def test_returns_every_functional_area_of_an_ambiguous_code(db):
    MetierDjangoFactory(offer_family_code="ERJUS008", domaine_fonctionnel_code="JUS")
    MetierDjangoFactory(offer_family_code="ERJUS008", domaine_fonctionnel_code="JUS")
    MetierDjangoFactory(offer_family_code="ERJUS008", domaine_fonctionnel_code="CTL")

    assert get_metier_functional_areas("ERJUS008") == {"JUS", "CTL"}


def test_ignores_archived_metiers_of_an_active_code(db):
    MetierDjangoFactory(offer_family_code="ERTRA007", domaine_fonctionnel_code="TRA")
    MetierDjangoFactory(
        offer_family_code="ERTRA007",
        domaine_fonctionnel_code="SEC",
        archived_at=timezone.now(),
    )

    assert get_metier_functional_areas("ERTRA007") == {"TRA"}


def test_uses_archived_metiers_without_active_one(db):
    MetierDjangoFactory(
        offer_family_code="ERTRA007",
        domaine_fonctionnel_code="SEC",
        archived_at=timezone.now(),
    )

    assert get_metier_functional_areas("ERTRA007") == {"SEC"}


def test_returns_an_empty_set_for_an_unknown_code(db):
    assert get_metier_functional_areas("ERNUM999") == set()
