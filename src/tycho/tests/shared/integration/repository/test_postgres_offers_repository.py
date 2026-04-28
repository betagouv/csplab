from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from django.db import DatabaseError
from faker import Faker
from pydantic import HttpUrl

from domain.entities.offer import Offer
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.factories.offer_factory import OfferFactory

fake = Faker()
NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOffersRepository(LoggerService())


class TestFindByIds:
    @pytest.mark.parametrize("ids", [[], [fake.uuid4()]])
    def test_empty_or_unknown_ids(self, db, repository, ids):
        assert repository.get_by_ids(ids) == []

    def test_return_correct_list_of_existing_ids(self, db, repository):
        offer = OfferFactory.create_batch(3)
        expected_ids = [offer[i].id for i in range(2)]

        results = repository.get_by_ids(expected_ids)

        assert {doc.id for doc in results} == set(expected_ids)
        for doc in results:
            assert isinstance(doc, Offer)


class TestUpsertBatch:
    def test_datetime_on_upsert(self, db, repository):
        offer = OfferFactory.create()
        offer_to_update = OfferFactory.create()
        new_offer = OfferFactory.create(save_in_db=False)

        offers = [
            OfferModel.to_entity(offer_to_update),
            OfferModel.to_entity(new_offer),
        ]

        timestamps = {
            offer: (offer.created_at, offer.updated_at),
            offer_to_update: (
                offer_to_update.created_at,
                offer_to_update.updated_at,
            ),
        }

        OfferModel.objects.get(external_id=offer.external_id)
        OfferModel.objects.get(external_id=offer_to_update.external_id)
        assert not OfferModel.objects.filter(external_id=new_offer.external_id).exists()

        repository.upsert_batch(offers)

        created_at, updated_at = timestamps[offer]
        offer.refresh_from_db()
        assert offer.created_at == created_at
        assert offer.updated_at == updated_at

        created_at, updated_at = timestamps[offer_to_update]
        offer_to_update.refresh_from_db()
        assert offer_to_update.created_at == created_at
        assert offer_to_update.updated_at > updated_at

        assert OfferModel.objects.filter(external_id=new_offer.external_id).exists()

    def test_upsert_raises_error(self, db, repository):
        with pytest.raises(DatabaseError):
            repository.upsert_batch([{"dummy": "object"}])

    def test_upsert_batch_with_empty_offers_list(self, db, repository):
        result = repository.upsert_batch([])

        assert result == {"created": 0, "updated": 0, "errors": []}

    def test_multiple_offers_success(self, db, repository):
        offers = OfferFactory.create_batch(2) + [OfferFactory.create(save_in_db=False)]
        entities = [OfferModel.to_entity(offer) for offer in offers]

        result = repository.upsert_batch(entities)

        assert result == {"created": 1, "updated": 2, "errors": []}

        external_ids = [e.external_id for e in entities]
        saved_offers = OfferModel.objects.filter(external_id__in=external_ids)
        saved_by_id = {o.external_id: o for o in saved_offers}

        for entity in entities:
            saved = saved_by_id[entity.external_id]
            assert OfferModel.to_entity(saved) == entity

    def test_updated_datas_are_stored(self, db, repository):
        offer = OfferFactory.create(
            verse=Verse.FPT,
            title="old title",
            profile="old  profile",
            mission="old mission",
            category=Category.B,
            contract_type=ContractType.CONTRACTUELS,
            organization="old organization",
            offer_url="https://fake.url/old",
            country="FRA",
            region="28",
            department="14",
            publication_date=datetime(2025, 5, 17),
            beginning_date=LimitDate(datetime(2025, 6, 17)),
        )
        now = datetime.now(timezone.utc)
        entity = OfferModel.to_entity(offer)
        updated_fields = {
            "verse": Verse.FPE,
            "title": "title",
            "profile": "profile",
            "mission": "mission",
            "category": Category.A,
            "contract_type": ContractType.TITULAIRE_CONTRACTUEL,
            "organization": "organization",
            "offer_url": HttpUrl("https://fake.url/offer"),
            "localisation": Localisation(
                country=Country("GUF"),
                region=Region(code="03"),
                department=Department(code="973"),
            ),
            "publication_date": now,
            "beginning_date": LimitDate(now),
        }
        for field, value in updated_fields.items():
            setattr(entity, field, value)

        result = repository.upsert_batch([entity])
        assert result == {"created": 0, "updated": 1, "errors": []}

        saved_offer = OfferModel.objects.get()
        assert OfferModel.to_entity(saved_offer) == entity


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        OfferFactory.create(archived_at=NOW)
        OfferFactory.create(processing=True)
        OfferFactory.create(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = OfferFactory.create()
        updated_after_processed = OfferFactory.create(
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
        OfferFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert OfferModel.objects.filter(processing=True).count() == 1
        assert OfferModel.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    offers = [
        OfferFactory.create(processing=True).to_entity(),
        OfferFactory.create(processing=False).to_entity(),
    ]
    undesired_offer = OfferFactory.create(processing=True).to_entity()

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
        OfferFactory.create(processing=True).to_entity(),
        OfferFactory.create(processing=False).to_entity(),
    ]
    undesired_offer = OfferFactory.create(processing=True).to_entity()

    count = repository.mark_as_pending(offers)
    assert count == len(offers)

    model_objects = OfferModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        offer.id for offer in offers
    }

    undesired_model_objects = OfferModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_offer.id
