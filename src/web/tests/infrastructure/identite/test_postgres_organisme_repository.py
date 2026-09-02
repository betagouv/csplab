from datetime import datetime, timezone

from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.repositories.identite.postgres_organisme_repository import (
    PostgresOrganismeRepository,
)


def test_create_seeds_created_at_from_historical_date_creation(db):
    date_creation = datetime(2018, 3, 12, tzinfo=timezone.utc)
    organisme = OrganismeFactory.create_entity(date_creation=date_creation)
    repository = PostgresOrganismeRepository()

    repository.create(organisme)

    model = OrganismeModel.objects.get(id=organisme.entity_id)
    assert model.created_at == date_creation
    assert model.date_creation == date_creation
