from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta

from domain.entities.corps import Corps
from infrastructure.django_apps.shared.models.corps import CorpsModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)
from tests.factories.corps_factory import CorpsFactory

NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresCorpsRepository(LoggerService())


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        CorpsFactory.create(archived_at=NOW)
        CorpsFactory.create(processing=True)
        CorpsFactory.create(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = CorpsFactory.create()
        updated_after_processed = CorpsFactory.create(
            processed_at=DAY_AGO, updated_at=NOW
        )

        entities = repository.get_pending_processing()
        assert {e.id for e in entities} == {
            never_processed.id,
            updated_after_processed.id,
        }

        for entity in entities:
            assert isinstance(entity, Corps)
            assert entity.processing

    def test_limit(self, db, repository):
        CorpsFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert CorpsModel.objects.filter(processing=True).count() == 1
        assert CorpsModel.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    corps_list = [
        CorpsFactory.create(processing=True).to_entity(),
        CorpsFactory.create(processing=False).to_entity(),
    ]
    undesired_corps = CorpsFactory.create(processing=True).to_entity()

    count = repository.mark_as_processed(corps_list)
    assert count == len(corps_list)

    model_objects = CorpsModel.objects.filter(
        processing=False, processed_at__isnull=False
    )
    assert set(model_objects.values_list("id", flat=True)) == {
        corps.id for corps in corps_list
    }

    undesired_model_objects = CorpsModel.objects.get(
        processing=True, processed_at__isnull=True
    )
    assert undesired_model_objects.id == undesired_corps.id


def test_mark_as_pending(db, repository):
    corps_list = [
        CorpsFactory.create(processing=True).to_entity(),
        CorpsFactory.create(processing=False).to_entity(),
    ]
    undesired_corps = CorpsFactory.create(processing=True).to_entity()

    count = repository.mark_as_pending(corps_list)
    assert count == len(corps_list)

    model_objects = CorpsModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        corps.id for corps in corps_list
    }

    undesired_model_objects = CorpsModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_corps.id
