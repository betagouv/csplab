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

        assert ApiLogModel.objects.count() == 1
        saved = ApiLogModel.objects.get(id=api_log.id)
        assert saved.path == api_log.path
        assert saved.ip_address == api_log.ip_address
        assert saved.method == api_log.method
        assert saved.status_code == api_log.status_code
        assert saved.auth_token == api_log.auth_token
        assert saved.token_type == api_log.token_type

    def test_multiple_logs_are_independent(self, db, repository):
        log_a = ApiLogFactory.create_entity(path="/api/v1/offres/")
        log_b = ApiLogFactory.create_entity(path="/api/v1/sources/")

        repository.save(log_a)
        repository.save(log_b)

        assert ApiLogModel.objects.count() == 2  # noqa: PLR2004

    def test_roundtrip_to_entity(self, db, repository):
        api_log = ApiLogFactory.create_entity()

        repository.save(api_log)

        model = ApiLogModel.objects.get(id=api_log.id)
        restored = model.to_entity()
        assert restored.id == api_log.id
        assert restored.path == api_log.path
        assert restored.ip_address == api_log.ip_address
        assert restored.method == api_log.method
        assert restored.status_code == api_log.status_code
        assert restored.auth_token == api_log.auth_token
        assert restored.token_type == api_log.token_type
