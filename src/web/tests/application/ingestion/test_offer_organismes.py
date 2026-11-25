import pytest
from django.utils import timezone

from application.ingestion.context_services.offer_organismes import OfferOrganismes
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)

pytestmark = pytest.mark.django_db


def test_finds_the_organisme_of_a_siret_once(django_assert_num_queries):
    organisme = OrganismeDjangoFactory()
    offer_organismes = OfferOrganismes()

    with django_assert_num_queries(1):
        assert offer_organismes.organisme_id(organisme.siret) == organisme.id
        assert offer_organismes.organisme_id(organisme.siret) == organisme.id


def test_ignores_deleted_and_unknown_organismes(django_assert_num_queries):
    deleted = OrganismeDjangoFactory(supprime_le=timezone.now())
    offer_organismes = OfferOrganismes()

    with django_assert_num_queries(2):
        assert offer_organismes.organisme_id(deleted.siret) is None
        assert offer_organismes.organisme_id("73282932000074") is None
        assert offer_organismes.organisme_id("73282932000074") is None


def test_checks_a_talentsoft_organisme_once(django_assert_num_queries):
    entity_code = TalentsoftOrganismeDjangoFactory().entity_code
    offer_organismes = OfferOrganismes()

    with django_assert_num_queries(2):
        assert offer_organismes.talentsoft_organisme_exists(entity_code)
        assert offer_organismes.talentsoft_organisme_exists(entity_code)
        assert not offer_organismes.talentsoft_organisme_exists("INCONNU")
        assert not offer_organismes.talentsoft_organisme_exists("INCONNU")
