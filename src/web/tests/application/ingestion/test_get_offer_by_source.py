from datetime import UTC, datetime
from uuid import uuid4

import pytest

from application.ingestion.errors.application_errors_ingestion import (
    OffreIntrouvable,
    SourceNonAutorisee,
)
from application.ingestion.services.get_offer_by_source import get_offer_by_source
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


@pytest.fixture
def source(db):
    return SourceDjangoFactory()


@pytest.fixture
def user(source):
    return UtilisateurDjangoFactory(sources=[source])


def test_refuses_a_source_the_user_is_not_linked_to(user):
    other = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=other)

    with pytest.raises(SourceNonAutorisee):
        get_offer_by_source(user, other.source_id, offer.id)


def test_refuses_an_offer_of_another_source(user, source):
    offer = OfferDjangoFactory(source=SourceDjangoFactory())

    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(user, source.source_id, offer.id)


def test_refuses_an_archived_offer(user, source):
    offer = OfferDjangoFactory(
        source=source, archived_at=datetime(2024, 2, 1, tzinfo=UTC)
    )

    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(user, source.source_id, offer.id)


def test_refuses_an_unknown_offer(user, source):
    with pytest.raises(OffreIntrouvable):
        get_offer_by_source(user, source.source_id, uuid4())
