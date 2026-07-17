from datetime import datetime

import pytest
from dateutil.relativedelta import relativedelta
from faker import Faker
from referentiel.entities.metier import Metier

from infrastructure.django_apps.referentiel.models.metier import MetierModel
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.metier_mapper import MetierMapper
from infrastructure.repositories.shared.postgres_metier_repository import (
    PostgresMetierRepository,
)
from tests.factories.referentiel.metier_factory import MetierFactory

fake = Faker()
NOW = datetime.now()
DAY_AGO = NOW - relativedelta(days=1)

_mapper = MetierMapper()


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresMetierRepository(LoggerService(), _mapper)


class TestGetPendingProcessing:
    def test_excluded_items(self, db, repository):
        MetierFactory.create_model(archived_at=NOW)
        MetierFactory.create_model(processing=True)
        MetierFactory.create_model(processed_at=NOW, updated_at=DAY_AGO)

        assert repository.get_pending_processing() == []

    def test_get_pending_items_with_logical_lock(self, db, repository):
        never_processed = MetierFactory.create_model()
        updated_after_processed = MetierFactory.create_model(
            processed_at=DAY_AGO, updated_at=NOW
        )

        entities = repository.get_pending_processing()
        assert {e.id for e in entities} == {
            never_processed.id,
            updated_after_processed.id,
        }

        for entity in entities:
            assert isinstance(entity, Metier)

    def test_limit(self, db, repository):
        MetierFactory.create_model_batch(2)

        entities = repository.get_pending_processing(limit=1)
        assert len(entities) == 1
        assert MetierModel.objects.filter(processing=True).count() == 1
        assert MetierModel.objects.filter(processing=False).count() == 1


def test_mark_as_processed(db, repository):
    concours_list = [
        _mapper.to_domain(MetierFactory.create_model(processing=True)),
        _mapper.to_domain(MetierFactory.create_model(processing=False)),
    ]
    undesired_concours = _mapper.to_domain(MetierFactory.create_model(processing=True))

    count = repository.mark_as_processed(concours_list)
    assert count == len(concours_list)

    model_objects = MetierModel.objects.filter(
        processing=False, processed_at__isnull=False
    )
    assert set(model_objects.values_list("id", flat=True)) == {
        concours.id for concours in concours_list
    }

    undesired_model_objects = MetierModel.objects.get(
        processing=True, processed_at__isnull=True
    )
    assert undesired_model_objects.id == undesired_concours.id


def test_mark_as_pending(db, repository):
    metiers_list = [
        _mapper.to_domain(MetierFactory.create_model(processing=True)),
        _mapper.to_domain(MetierFactory.create_model(processing=False)),
    ]
    undesired_metiers = _mapper.to_domain(MetierFactory.create_model(processing=True))

    count = repository.mark_as_pending(metiers_list)
    assert count == len(metiers_list)

    model_objects = MetierModel.objects.filter(processing=False)
    assert set(model_objects.values_list("id", flat=True)) == {
        metier.id for metier in metiers_list
    }

    undesired_model_objects = MetierModel.objects.get(processing=True)
    assert undesired_model_objects.id == undesired_metiers.id
