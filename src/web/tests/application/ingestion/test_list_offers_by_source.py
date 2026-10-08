from uuid import uuid4

import pytest

from application.ingestion.errors.application_errors_ingestion import (
    SourceNonAutorisee,
)
from application.ingestion.services.list_offers_by_source import list_offers_by_source
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
def user(db):
    return UtilisateurDjangoFactory(sources=[SourceDjangoFactory()])


def test_refuses_a_source_the_user_is_not_linked_to(user):
    other = SourceDjangoFactory()
    OfferDjangoFactory(source=other)

    with pytest.raises(SourceNonAutorisee):
        list_offers_by_source(user, other.source_id)


def test_refuses_an_unknown_source(user):
    with pytest.raises(SourceNonAutorisee):
        list_offers_by_source(user, uuid4())
