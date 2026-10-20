from datetime import UTC, datetime
from uuid import uuid4

import pytest

from application.ingestion.errors.application_errors_ingestion import (
    OffreIntrouvable,
    SourceIntrouvable,
)
from application.ingestion.services.get_offer_by_source import get_offer_by_source
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


@pytest.fixture
def source(db):
    return SourceDjangoFactory()


def test_returns_the_offer_of_the_source(source):
    offer = OfferDjangoFactory(source=source)

    assert get_offer_by_source(source.source_id, offer.id) == offer


def test_refuses_an_unknown_source(db):
    offer = OfferDjangoFactory()

    with pytest.raises(SourceIntrouvable):
        get_offer_by_source(uuid4(), offer.id)


def test_refuses_an_offer_of_another_source(source):
    offer = OfferDjangoFactory(source=SourceDjangoFactory())

    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(source.source_id, offer.id)


def test_refuses_an_archived_offer(source):
    offer = OfferDjangoFactory(
        source=source, archived_at=datetime(2024, 2, 1, tzinfo=UTC)
    )

    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(source.source_id, offer.id)


def test_refuses_an_unknown_offer(source):
    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(source.source_id, uuid4())
