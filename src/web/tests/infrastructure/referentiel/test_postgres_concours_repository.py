from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from faker import Faker
from referentiel.entities.concours import Concours

from infrastructure.django_apps.referentiel.models.concours import ConcoursModel
from infrastructure.factories.referentiel.concours_django_factory import (
    ConcoursDjangoFactory,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.shared.postgres_concours_repository import (
    PostgresConcoursRepository,
)

fake = Faker()
NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresConcoursRepository(LoggerService())


class TestFindByIds:
    @pytest.mark.parametrize("ids", [[], [fake.uuid4()]])
    def test_empty_or_unknown_ids(self, db, repository, ids):
        assert repository.get_by_ids(ids) == []

    def test_return_correct_list_of_existing_ids(self, db, repository):
        concours = ConcoursDjangoFactory.create_batch(3)
        expected_ids = [concours[i].id for i in range(2)]

        results = repository.get_by_ids(expected_ids)

        assert {doc.id for doc in results} == set(expected_ids)
        for doc in results:
            assert isinstance(doc, Concours)


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        ConcoursDjangoFactory(archived_at=NOW)
        ConcoursDjangoFactory(processing=True)
        ConcoursDjangoFactory(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = ConcoursDjangoFactory()
        updated_after_processed = ConcoursDjangoFactory(
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
        ConcoursDjangoFactory.create_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert ConcoursModel.objects.filter(processing=True).count() == 1
        assert ConcoursModel.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    concours_list = [
        ConcoursDjangoFactory(processing=True).to_entity(),
        ConcoursDjangoFactory(processing=False).to_entity(),
    ]
    undesired_concours = ConcoursDjangoFactory(processing=True).to_entity()

    count = repository.mark_as_processed(concours_list)
    assert count == len(concours_list)

    model_objects = ConcoursModel.objects.filter(
        processing=False, processed_at__isnull=False
    )
    assert set(model_objects.values_list("id", flat=True)) == {
        concours.id for concours in concours_list
    }

    undesired_model_objects = ConcoursModel.objects.get(
        processing=True, processed_at__isnull=True
    )
    assert undesired_model_objects.id == undesired_concours.id


def test_mark_as_pending(db, repository):
    concours_list = [
        ConcoursDjangoFactory(processing=True).to_entity(),
        ConcoursDjangoFactory(processing=False).to_entity(),
    ]
    undesired_concours = ConcoursDjangoFactory(processing=True).to_entity()

    count = repository.mark_as_pending(concours_list)
    assert count == len(concours_list)

    model_objects = ConcoursModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        concours.id for concours in concours_list
    }

    undesired_model_objects = ConcoursModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_concours.id
