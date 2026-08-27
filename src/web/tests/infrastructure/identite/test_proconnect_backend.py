from unittest.mock import MagicMock

import pytest

from infrastructure.authentication.proconnect_backend import ProconnectBackend
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


@pytest.fixture(name="backend")
def backend_fixture():
    return ProconnectBackend()


class TestProconnectBackend:
    def test_authenticate_matches_existing_email(self, db, backend):
        user = UtilisateurFactory.create_model()

        authenticated = backend.authenticate(
            None, proconnect_claims={"email": user.email}
        )

        assert authenticated == user

    def test_authenticate_returns_none_for_unknown_email(self, db, backend):
        authenticated = backend.authenticate(
            None, proconnect_claims={"email": "unknown@example.com"}
        )

        assert authenticated is None

    def test_authenticate_returns_none_without_claims(self, db, backend):
        assert backend.authenticate(None, proconnect_claims=None) is None
        assert backend.authenticate(None, proconnect_claims={}) is None

    def test_audit_connexion_logs_the_login(self, db, backend):
        user = UtilisateurFactory.create_model()

        backend._audit_connexion(user)

        audit_log_repository = backend.container.postgres_audit_log_repository()
        entity = UtilisateurMapper().to_domain(user)
        logs = audit_log_repository.get_logs_for_ressource(
            "Utilisateur", entity.entity_id
        )
        assert len(logs) == 1
        assert logs[0].event_name == "Connexion"

    def test_audit_connexion_swallows_errors(self, db, backend):
        user = UtilisateurFactory.create_model()
        failing_usecase = MagicMock()
        failing_usecase.execute.side_effect = RuntimeError("boom")
        backend.container.log_utilisateur_connexion_usecase.override(failing_usecase)

        backend._audit_connexion(user)
