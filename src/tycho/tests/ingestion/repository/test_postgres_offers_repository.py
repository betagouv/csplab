from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from domain.entities.offer import Offer
from infrastructure.django_apps.shared.models.offer import OfferModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_offers_repository import (
    PostgresOffersRepository,
)
from tests.factories.offer_factory import OfferFactory

NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresOffersRepository(LoggerService())


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
