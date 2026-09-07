from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from referentiel.entities.corps import Corps

from infrastructure.django_apps.referentiel.models.corps import CorpsModel
from infrastructure.factories.referentiel.corps_django_factory import (
    CorpsDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_corps_repository import (
    PostgresCorpsRepository,
)

NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresCorpsRepository(LoggerService())


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        CorpsDjangoFactory(archived_at=NOW)
        CorpsDjangoFactory(processing=True)
        CorpsDjangoFactory(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = CorpsDjangoFactory()
        updated_after_processed = CorpsDjangoFactory(
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
        CorpsDjangoFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert CorpsModel.objects.filter(processing=True).count() == 1
        assert CorpsModel.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    corps_list = [
        CorpsDjangoFactory(processing=True).to_entity(),
        CorpsDjangoFactory(processing=False).to_entity(),
    ]
    undesired_corps = CorpsDjangoFactory(processing=True).to_entity()

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
        CorpsDjangoFactory(processing=True).to_entity(),
        CorpsDjangoFactory(processing=False).to_entity(),
    ]
    undesired_corps = CorpsDjangoFactory(processing=True).to_entity()

    count = repository.mark_as_pending(corps_list)
    assert count == len(corps_list)

    model_objects = CorpsModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        corps.id for corps in corps_list
    }

    undesired_model_objects = CorpsModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_corps.id
