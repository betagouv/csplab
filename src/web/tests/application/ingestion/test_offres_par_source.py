from datetime import UTC, datetime

import pytest

from application.ingestion.services.offres_par_source import list_source_offers
from domain.ingestion.exceptions.source_authorization_error import (
    SourceAuthorizationError,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


def test_lists_the_active_offers_of_the_source(db):
    source = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=source)
    OfferDjangoFactory(source=source, archived_at=datetime.now(UTC))
    OfferDjangoFactory()

    assert list(list_source_offers(source.source_id, None)) == [offer]


def test_lists_the_offers_of_a_source_of_the_user(db):
    source = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=source)
    user = UtilisateurDjangoFactory()
    user.sources.add(source)

    assert list(list_source_offers(source.source_id, user)) == [offer]


def test_lets_a_superuser_list_any_source(db):
    source = SourceDjangoFactory()
    offer = OfferDjangoFactory(source=source)

    user = UtilisateurDjangoFactory(is_superuser=True)

    assert list(list_source_offers(source.source_id, user)) == [offer]


def test_refuses_a_source_of_another_user(db):
    source = SourceDjangoFactory()

    with pytest.raises(SourceAuthorizationError):
        list_source_offers(source.source_id, UtilisateurDjangoFactory())


def test_reads_the_siret_of_the_talentsoft_organisme(db):
    organisme = OrganismeDjangoFactory()
    offer = OfferDjangoFactory(
        talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory(
            organisme=organisme
        )
    )

    (listed,) = list_source_offers(offer.source_id, None)

    assert listed.organisation_siret == organisme.siret
