from uuid import uuid4

import pytest

from application.ingestion.errors.application_errors_ingestion import (
    SourceIntrouvable,
)
from application.ingestion.services.list_offers_by_source import list_offers_by_source
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_lists_the_offers_of_any_source(db):
    source = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=source)
    OfferDjangoFactory()

    assert list(list_offers_by_source(source.source_id)) == [offer]


def test_refuses_an_unknown_source(db):
    with pytest.raises(SourceIntrouvable):
        list_offers_by_source(uuid4())
