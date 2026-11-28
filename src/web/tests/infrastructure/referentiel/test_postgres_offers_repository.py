from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from faker import Faker
from referentiel.entities.offer import Offer
from referentiel.exceptions.offer_errors import (
    MultipleOffersFoundForReference,
    OfferDoesNotExist,
)

from infrastructure.django_apps.referentiel.models.offer import OfferModel
from infrastructure.factories.ingestion.talentsoft_organisme_django_factory import (
    TalentsoftOrganismeDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.offer_mapper import OfferMapper
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)

fake = Faker()
NOW = datetime.now(timezone.utc)
DAY_AGO = NOW - relativedelta(days=1)

_mapper = OfferMapper()


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOffersRepository(LoggerService(), _mapper)


def _create_offers_with_two_localisations() -> list[OfferModel]:
    localisations = [
        {"area": "EU", "country": "FRA", "region": "28", "department": "14"},
        {"area": "EU", "country": "FRA", "region": "84", "department": "69"},
    ]
    return OfferDjangoFactory.create_batch(2, localisations=localisations)


class TestFindByIds:
    @pytest.mark.parametrize("ids", [[], [fake.uuid4()]])
    def test_empty_or_unknown_ids(self, db, repository, ids):
        assert repository.get_by_ids(ids) == []

    def test_return_correct_list_of_existing_ids(self, db, repository):
        offer = OfferDjangoFactory.create_batch(3)
        expected_ids = [offer[i].id for i in range(2)]

        results = repository.get_by_ids(expected_ids)

        assert {doc.id for doc in results} == set(expected_ids)
        for doc in results:
            assert isinstance(doc, Offer)

    def test_prefetches_localisations(self, db, repository, django_assert_num_queries):
        offers = _create_offers_with_two_localisations()

        with django_assert_num_queries(
            1  # select the offers
            + 1  # prefetch their localisations
        ):
            results = repository.get_by_ids([offer.id for offer in offers])

        assert [len(offer.localisations) for offer in results] == [2, 2]


def test_get_all_prefetches_localisations(db, repository, django_assert_num_queries):
    _create_offers_with_two_localisations()

    with django_assert_num_queries(
        1  # select the offers
        + 1  # prefetch their localisations
    ):
        results = repository.get_all()

    assert [len(offer.localisations) for offer in results] == [2, 2]


class TestGetFilteredByGeo:
    def test_filters_offers_within_radius(self, db, repository):
        paris = OfferDjangoFactory(
            country="FRA",
            region="11",
            department="75",
            latitude=48.8566,
            longitude=2.3522,
        )
        lyon = OfferDjangoFactory(
            country="FRA",
            region="84",
            department="69",
            latitude=45.7640,
            longitude=4.8357,
        )
        OfferDjangoFactory(
            country="FRA",
            region="11",
            department="75",
        )

        page = repository.get_filtered(
            active=True,
            latitude=48.8566,
            longitude=2.3522,
            radius_km=50,
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {paris.id}
        assert lyon.id not in ids

    def test_widening_radius_includes_more_offers(self, db, repository):
        paris = OfferDjangoFactory(
            country="FRA",
            region="11",
            department="75",
            latitude=48.8566,
            longitude=2.3522,
        )
        lyon = OfferDjangoFactory(
            country="FRA",
            region="84",
            department="69",
            latitude=45.7640,
            longitude=4.8357,
        )

        page = repository.get_filtered(
            active=True,
            latitude=48.8566,
            longitude=2.3522,
            radius_km=500,
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {paris.id, lyon.id}

    def test_ignores_geo_filter_when_not_fully_provided(self, db, repository):
        OfferDjangoFactory(
            country="FRA",
            region="11",
            department="75",
            latitude=48.8566,
            longitude=2.3522,
        )

        page = repository.get_filtered(
            active=True,
            latitude=48.8566,
        )

        assert page.count() == 1


class TestGetFilteredByDomain:
    def test_filters_offers_by_single_domain(self, db, repository):
        numerique = OfferDjangoFactory(functional_area_code="NUM")
        OfferDjangoFactory(functional_area_code="ACH")

        page = repository.get_filtered(
            active=True,
            domain=["NUM"],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {numerique.id}

    def test_filters_offers_by_multiple_domains(self, db, repository):
        numerique = OfferDjangoFactory(functional_area_code="NUM")
        achat = OfferDjangoFactory(functional_area_code="ACH")
        OfferDjangoFactory(functional_area_code="JUR")

        page = repository.get_filtered(
            active=True,
            domain=["NUM", "ACH"],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {numerique.id, achat.id}

    def test_no_domain_filter_returns_all_offers(self, db, repository):
        offers = OfferDjangoFactory.create_batch(2)

        page = repository.get_filtered(
            active=True,
        )

        assert page.count() == len(offers)


class TestGetFilteredByOrganization:
    def test_filters_offers_by_single_organization(self, db, repository):
        organisme = TalentsoftOrganismeDjangoFactory()
        offer = OfferDjangoFactory(talentsoft_organisme_entity_code=organisme)
        OfferDjangoFactory(
            talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory()
        )
        OfferDjangoFactory(talentsoft_organisme_entity_code=None)

        page = repository.get_filtered(
            active=True,
            organization=[organisme.entity_code],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {offer.id}

    def test_filters_offers_by_multiple_organizations(self, db, repository):
        organisme_a = TalentsoftOrganismeDjangoFactory()
        organisme_b = TalentsoftOrganismeDjangoFactory()
        offer_a = OfferDjangoFactory(talentsoft_organisme_entity_code=organisme_a)
        offer_b = OfferDjangoFactory(talentsoft_organisme_entity_code=organisme_b)
        OfferDjangoFactory(
            talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory()
        )

        page = repository.get_filtered(
            active=True,
            organization=[organisme_a.entity_code, organisme_b.entity_code],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {offer_a.id, offer_b.id}

    def test_includes_offers_of_child_organizations(self, db, repository):
        parent = TalentsoftOrganismeDjangoFactory(has_children=True)
        child_b = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        child_c = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        other = TalentsoftOrganismeDjangoFactory()
        offer_a = OfferDjangoFactory(talentsoft_organisme_entity_code=parent)
        offer_b = OfferDjangoFactory(talentsoft_organisme_entity_code=child_b)
        offer_c = OfferDjangoFactory(talentsoft_organisme_entity_code=child_c)
        OfferDjangoFactory(talentsoft_organisme_entity_code=other)

        page = repository.get_filtered(
            active=True,
            organization=[parent.entity_code],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {offer_a.id, offer_b.id, offer_c.id}

    def test_includes_offers_of_all_descendant_organizations(self, db, repository):
        parent = TalentsoftOrganismeDjangoFactory(has_children=True)
        child = TalentsoftOrganismeDjangoFactory(
            parent_code=parent.code, has_children=True
        )
        grandchild = TalentsoftOrganismeDjangoFactory(parent_code=child.code)
        offer_parent = OfferDjangoFactory(talentsoft_organisme_entity_code=parent)
        offer_child = OfferDjangoFactory(talentsoft_organisme_entity_code=child)
        offer_grandchild = OfferDjangoFactory(
            talentsoft_organisme_entity_code=grandchild
        )

        page = repository.get_filtered(
            active=True,
            organization=[parent.entity_code],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {offer_parent.id, offer_child.id, offer_grandchild.id}

    def test_child_organization_does_not_include_its_parent(self, db, repository):
        parent = TalentsoftOrganismeDjangoFactory(has_children=True)
        child = TalentsoftOrganismeDjangoFactory(parent_code=parent.code)
        OfferDjangoFactory(talentsoft_organisme_entity_code=parent)
        offer_child = OfferDjangoFactory(talentsoft_organisme_entity_code=child)

        page = repository.get_filtered(
            active=True,
            organization=[child.entity_code],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {offer_child.id}

    def test_unknown_organization_returns_no_offers(self, db, repository):
        OfferDjangoFactory(
            talentsoft_organisme_entity_code=TalentsoftOrganismeDjangoFactory()
        )

        page = repository.get_filtered(
            active=True,
            organization=["INCONNU"],
        )

        assert page.count() == 0

    def test_no_organization_filter_returns_all_offers(self, db, repository):
        offers = OfferDjangoFactory.create_batch(2)

        page = repository.get_filtered(
            active=True,
        )

        assert page.count() == len(offers)


class TestGetFilteredByPublicationDate:
    def test_filters_offers_published_within_the_last_n_days(self, db, repository):
        recent = OfferDjangoFactory(publication_date=NOW - relativedelta(days=2))
        OfferDjangoFactory(publication_date=NOW - relativedelta(days=30))

        page = repository.get_filtered(
            active=True,
            published_within_days=-7,
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {recent.id}

    def test_no_publication_date_filter_returns_all_offers(self, db, repository):
        offers = OfferDjangoFactory.create_batch(2)

        page = repository.get_filtered(
            active=True,
        )

        assert page.count() == len(offers)


class TestGetFilteredByKeywords:
    def test_filters_offers_matching_keywords_in_title(self, db, repository):
        developpeur = OfferDjangoFactory(
            title="Développeur informatique",
            mission="Développement d'applications web",
        )
        OfferDjangoFactory(
            title="Jardinier paysagiste", mission="Entretien des espaces verts"
        )

        page = repository.get_filtered(
            active=True,
            keywords="développeur",
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {developpeur.id}

    def test_matches_across_multiple_fields(self, db, repository):
        offer = OfferDjangoFactory(
            title="Chargé de mission",
            organization="Mairie de Bordeaux",
        )
        OfferDjangoFactory(title="Chargé de mission", organization="Mairie de Nantes")

        page = repository.get_filtered(
            active=True,
            keywords="Bordeaux",
        )

        ids = {o.id for o in page.slice(0, 10)}
        assert ids == {offer.id}

    def test_no_match_returns_empty_page(self, db, repository):
        OfferDjangoFactory(title="Développeur informatique")

        page = repository.get_filtered(
            active=True,
            keywords="astrophysicien",
        )

        assert page.count() == 0

    def test_no_keywords_filter_returns_all_offers(self, db, repository):
        offers = OfferDjangoFactory.create_batch(2)

        page = repository.get_filtered(
            active=True,
        )

        assert page.count() == len(offers)

    def test_multiple_keywords_require_all_terms_to_match(self, db, repository):
        both_terms = OfferDjangoFactory(
            title="Développeur back-end Python",
        )
        OfferDjangoFactory(title="Développeur front-end JavaScript")
        OfferDjangoFactory(title="Chef de projet Python")

        page = repository.get_filtered(
            active=True,
            keywords="développeur python",
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {both_terms.id}

    def test_combines_with_another_filter(self, db, repository):
        matching = OfferDjangoFactory(
            title="Développeur informatique", functional_area_code="NUM"
        )
        OfferDjangoFactory(title="Développeur informatique", functional_area_code="ACH")
        OfferDjangoFactory(title="Jardinier paysagiste", functional_area_code="NUM")

        page = repository.get_filtered(
            active=True,
            keywords="développeur",
            domain=["NUM"],
        )

        ids = {offer.id for offer in page.slice(0, 10)}
        assert ids == {matching.id}

    def test_results_are_ranked_with_title_matches_first(self, db, repository):
        title_match = OfferDjangoFactory(
            title="Développeur informatique",
            mission="Gestion de projets divers",
        )
        mission_match = OfferDjangoFactory(
            title="Chargé de mission",
            mission="Encadrement d'une équipe de développeurs",
        )

        page = repository.get_filtered(
            active=True,
            keywords="développeur",
        )

        ids = [offer.id for offer in page.slice(0, 10)]
        assert ids == [title_match.id, mission_match.id]


class TestGetByReference:
    def test_returns_offer_with_matching_reference(self, db, repository):
        offer = OfferDjangoFactory(reference="REF-1")
        OfferDjangoFactory(reference="REF-2")

        result = repository.get_by_reference("REF-1")

        assert result.id == offer.id

    def test_unknown_reference_raises(self, db, repository):
        with pytest.raises(OfferDoesNotExist):
            repository.get_by_reference("UNKNOWN")

    def test_multiple_offers_sharing_reference_raises(self, db, repository):
        OfferDjangoFactory(reference="REF-1")
        OfferDjangoFactory(reference="REF-1")

        with pytest.raises(MultipleOffersFoundForReference):
            repository.get_by_reference("REF-1")


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        OfferDjangoFactory(archived_at=NOW)
        OfferDjangoFactory(processing=True)
        OfferDjangoFactory(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = OfferDjangoFactory()
        updated_after_processed = OfferDjangoFactory(
            processed_at=DAY_AGO, updated_at=NOW
        )

        entities = repository.get_pending_processing()
        assert {e.id for e in entities} == {
            never_processed.id,
            updated_after_processed.id,
        }

        for entity in entities:
            assert isinstance(entity, Offer)
            assert entity.processing

    def test_limit(self, db, repository):
        OfferDjangoFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert OfferModel.objects.filter(processing=True).count() == 1
        assert OfferModel.objects.filter(processing=False).count() == 1

    def test_prefetches_localisations(self, db, repository, django_assert_num_queries):
        _create_offers_with_two_localisations()

        with django_assert_num_queries(
            1  # savepoint of transaction.atomic
            + 1  # select the offers for update
            + 1  # mark them as processing
            + 1  # prefetch their localisations
            + 1  # release the savepoint
        ):
            entities = repository.get_pending_processing()

        assert [len(offer.localisations) for offer in entities] == [2, 2]


def test_mark_as_processed(db, repository):
    offers = [
        _mapper.to_domain(OfferDjangoFactory(processing=True)),
        _mapper.to_domain(OfferDjangoFactory(processing=False)),
    ]
    undesired_offer = _mapper.to_domain(OfferDjangoFactory(processing=True))

    count = repository.mark_as_processed(offers)
    assert count == len(offers)

    model_objects = OfferModel.objects.filter(
        processing=False, processed_at__isnull=False
    )
    assert set(model_objects.values_list("id", flat=True)) == {
        offer.id for offer in offers
    }

    undesired_model_objects = OfferModel.objects.get(
        processing=True, processed_at__isnull=True
    )
    assert undesired_model_objects.id == undesired_offer.id


def test_mark_as_pending(db, repository):
    offers = [
        _mapper.to_domain(OfferDjangoFactory(processing=True)),
        _mapper.to_domain(OfferDjangoFactory(processing=False)),
    ]
    undesired_offer = _mapper.to_domain(OfferDjangoFactory(processing=True))

    count = repository.mark_as_pending(offers)
    assert count == len(offers)

    model_objects = OfferModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        offer.id for offer in offers
    }

    undesired_model_objects = OfferModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_offer.id
