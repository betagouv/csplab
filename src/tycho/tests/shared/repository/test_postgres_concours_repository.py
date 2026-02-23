from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from domain.entities.concours import Concours
from infrastructure.django_apps.shared.models.concours import ConcoursModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)
from tests.factories.concours_factory import ConcoursFactory

NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresConcoursRepository(LoggerService())


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        ConcoursFactory.create(archived_at=NOW)
        ConcoursFactory.create(processing=True)
        ConcoursFactory.create(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = ConcoursFactory.create()
        updated_after_processed = ConcoursFactory.create(
            processed_at=DAY_AGO, updated_at=NOW
        )

        entities = repository.get_pending_processing()
        assert {e.id for e in entities} == {
            never_processed.id,
            updated_after_processed.id,
        }

        for entity in entities:
            assert isinstance(entity, Concours)
            assert entity.processing

    def test_limit(self, db, repository):
        ConcoursFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert ConcoursModel.objects.filter(processing=True).count() == 1
        assert ConcoursModel.objects.filter(processing=False).count() == 1
