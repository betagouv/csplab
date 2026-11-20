import pytest
from django.db import IntegrityError, transaction

from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_offer_without_category_is_rejected(db):
    with (
        pytest.raises(IntegrityError, match="offer_categories_not_empty"),
        transaction.atomic(),
    ):
        OfferDjangoFactory(categories=[])


def test_offer_with_long_title_equal_to_title_is_rejected(db):
    with (
        pytest.raises(IntegrityError, match="offer_long_title_differs_from_title"),
        transaction.atomic(),
    ):
        OfferDjangoFactory(title="Développeur", long_title="Développeur")


@pytest.mark.parametrize("long_title", [None, "Développeur back-end Python"])
def test_offer_with_long_title_absent_or_different_is_accepted(db, long_title):
    OfferDjangoFactory(title="Développeur", long_title=long_title)


def test_duplicate_localisation_abroad_is_rejected(db):
    berlin = {
        "area": "EU",
        "country": "DEU",
        "region": None,
        "department": None,
        "label": "Ambassade de France à Berlin",
    }
    with (
        pytest.raises(IntegrityError, match="offer_localisations_no_duplicate"),
        transaction.atomic(),
    ):
        OfferDjangoFactory(localisations=[berlin, berlin])


@pytest.mark.parametrize(
    "country, region, department",
    [
        ("str", "84", "01"),
        ("DEU", "84", None),
        ("FRA", None, None),
        ("FRA", "84", None),
    ],
)
def test_localisation_with_subdivision_inconsistent_with_country_is_rejected(
    db, country, region, department
):
    localisation = {
        "area": "EU",
        "country": country,
        "region": region,
        "department": department,
        "label": "",
    }
    with (
        pytest.raises(
            IntegrityError, match="offer_localisations_subdivision_in_france_only"
        ),
        transaction.atomic(),
    ):
        OfferDjangoFactory(localisations=[localisation])
