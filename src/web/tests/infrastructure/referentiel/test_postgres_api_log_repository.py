import pytest

from infrastructure.di.shared.shared_container import SharedContainer
from infrastructure.django_apps.shared.models.api_log import ApiLogModel
from tests.factories.api_log_factory import ApiLogFactory


@pytest.fixture
def repository():
    return SharedContainer().api_log_repository()


class TestSave:
    def test_persists_api_log(self, db, repository):
        api_log = ApiLogFactory.create_entity()

        repository.save(api_log)

        saved = ApiLogModel.objects.get()
        assert saved.to_entity() == api_log

    def test_multiple_logs_are_independent(self, db, repository):
        log_a = ApiLogFactory.create_entity(path="/api/v1/offres/")
        log_b = ApiLogFactory.create_entity(path="/api/v1/sources/")

        repository.save(log_a)
        repository.save(log_b)

        assert ApiLogModel.objects.count() == 2  # noqa: PLR2004
