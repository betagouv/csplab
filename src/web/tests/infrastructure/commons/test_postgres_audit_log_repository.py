from datetime import datetime, timezone
from uuid import uuid4

import pytest

from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.factories.commons.audit_log_factory import AuditLogFactory
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)


@pytest.fixture(name="repository")
def repository_fixture():
    return PostgresAuditLogRepository()


class TestStoreLog:
    def test_persists_audit_log(self, db, repository):
        audit_log = AuditLogFactory.create_entity()

        repository.store_log(audit_log)

        saved = AuditLogModel.objects.get()
        assert saved.to_entity() == audit_log

    def test_multiple_logs_are_independent(self, db, repository):
        event_names = ["ProfilAgentCree", "DossierCandidatureInitialise"]
        for event_name in event_names:
            repository.store_log(AuditLogFactory.create_entity(event_name=event_name))

        assert AuditLogModel.objects.count() == len(event_names)


class TestGetLogsForRessource:
    def test_returns_empty_list_when_no_logs(self, db, repository):
        result = repository.get_logs_for_ressource("Offre", uuid4())

        assert result == []

    def test_returns_logs_for_given_ressource(self, db, repository):
        ressource_id = uuid4()
        AuditLogFactory.create_model_batch(
            3, ressource_kind="Offre", ressource_id=ressource_id
        )

        result = repository.get_logs_for_ressource("Offre", ressource_id)

        assert len(result) == 3  # noqa: PLR2004

    def test_does_not_return_logs_for_other_resources(self, db, repository):
        expected_audit_log = AuditLogFactory.create_model(ressource_kind="Offre")
        AuditLogFactory.create_model(
            ressource_kind=expected_audit_log.ressource_kind, ressource_id=uuid4()
        )
        AuditLogFactory.create_model(
            ressource_kind="Candidature", ressource_id=expected_audit_log.ressource_id
        )

        result = repository.get_logs_for_ressource(
            expected_audit_log.ressource_kind, expected_audit_log.ressource_id
        )

        assert result == [expected_audit_log.to_entity()]

    def test_returns_logs_ordered_most_recent_first(self, db, repository):
        ressource_id = uuid4()
        older = AuditLogFactory.create_model(
            ressource_kind="Offre",
            ressource_id=ressource_id,
            occurred_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        newer = AuditLogFactory.create_model(
            ressource_kind="Offre",
            ressource_id=ressource_id,
            occurred_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
        )

        result = repository.get_logs_for_ressource("Offre", ressource_id)

        assert result[0].entity_id == newer.id
        assert result[1].entity_id == older.id
