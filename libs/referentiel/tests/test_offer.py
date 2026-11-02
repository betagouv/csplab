from datetime import UTC, datetime

import pytest
from pydantic import HttpUrl

from referentiel.entities.offer import Offer
from referentiel.exceptions.offer_errors import ConflictingApplicationChannelsError
from referentiel.value_objects.category import Category


def _offer(**overrides) -> Offer:
    return Offer(
        **{
            "title": "Titre",
            "profile": "Profil",
            "mission": "Mission",
            "organization": "Organisation",
            "verse": None,
            "categories": [],
            "offer_nature": None,
            "offer_url": None,
            "localisation": None,
            "publication_date": datetime(2026, 1, 1, tzinfo=UTC),
            "beginning_date": None,
            "reference": "REF-001",
            **overrides,
        }
    )


def test_offer_raises_when_application_url_and_email_are_both_set():
    with pytest.raises(ConflictingApplicationChannelsError):
        _offer(
            application_url=HttpUrl("https://exemple.gouv.fr/candidature"),
            application_email="rh@exemple.gouv.fr",
        )


@pytest.mark.parametrize(
    "application_url, application_email",
    [
        (HttpUrl("https://exemple.gouv.fr/candidature"), None),
        (None, "rh@exemple.gouv.fr"),
        (None, None),
    ],
)
def test_offer_accepts_at_most_one_application_channel(
    application_url, application_email
):
    offer = _offer(application_url=application_url, application_email=application_email)

    assert offer.application_url == application_url
    assert offer.application_email == application_email


@pytest.mark.parametrize(
    "categories, main_category",
    [
        ([Category.B, Category.A], Category.B),
        ([Category.C], Category.C),
        ([], None),
    ],
)
def test_offer_main_category_is_the_first_category(categories, main_category):
    assert _offer(categories=categories).main_category == main_category
