from unittest.mock import MagicMock

import pytest

from infrastructure.authentication.proconnect_backend import ProconnectBackend
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


@pytest.fixture(name="backend")
def backend_fixture():
    return ProconnectBackend()


class TestProconnectBackend:
    def test_authenticate_matches_existing_email(self, db, backend):
        user = UtilisateurDjangoFactory()

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

    def test_authenticate_fills_the_name_from_the_claims(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="", last_name="")

        authenticated = backend.authenticate(
            None,
            proconnect_claims={
                "email": user.email,
                "given_name": "Marie Claire",
                "usual_name": "Dupont",
            },
        )

        assert authenticated == user
        user.refresh_from_db()
        assert user.first_name == "Marie Claire"
        assert user.last_name == "Dupont"

    def test_sync_identite_updates_a_changed_name(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="Jean", last_name="Martin")

        backend._sync_identite(user, {"given_name": "Jean", "usual_name": "Durand"})

        user.refresh_from_db()
        assert user.last_name == "Durand"

    def test_sync_identite_does_not_write_when_nothing_changed(
        self, db, backend, django_assert_num_queries
    ):
        user = UtilisateurDjangoFactory(first_name="Jean", last_name="Martin")

        with django_assert_num_queries(0):
            backend._sync_identite(user, {"given_name": "Jean", "usual_name": "Martin"})

    def test_sync_identite_writes_only_the_changed_field(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="Jean", last_name="Martin")
        user.first_name = "modifie en memoire, jamais enregistre"

        backend._sync_identite(user, {"usual_name": "Durand"})

        user.refresh_from_db()
        assert user.last_name == "Durand"
        assert user.first_name == "Jean"

    def test_sync_identite_keeps_the_existing_value_without_claim(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="Jean", last_name="Martin")

        backend._sync_identite(user, {"given_name": "", "usual_name": None})

        user.refresh_from_db()
        assert user.first_name == "Jean"
        assert user.last_name == "Martin"

    def test_sync_identite_truncates_an_overlong_value(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="")
        longueur_max = user._meta.get_field("first_name").max_length

        backend._sync_identite(user, {"given_name": "a" * (longueur_max + 50)})

        user.refresh_from_db()
        assert user.first_name == "a" * longueur_max

    def test_sync_identite_swallows_errors(self, db, backend):
        user = UtilisateurDjangoFactory(first_name="Jean")
        user.save = MagicMock(side_effect=RuntimeError("boom"))
        backend.logger = MagicMock()

        backend._sync_identite(user, {"given_name": "Marie"})

        backend.logger.error.assert_called_once()
        user.refresh_from_db()
        assert user.first_name == "Jean"

    def test_audit_connexion_logs_the_login(self, db, backend):
        user = UtilisateurDjangoFactory()

        backend._audit_connexion(user)

        audit_log_repository = backend.container.postgres_audit_log_repository()
        entity = UtilisateurMapper().to_domain(user)
        logs = audit_log_repository.get_logs_for_ressource(
            "Utilisateur", entity.entity_id
        )
        assert len(logs) == 1
        assert logs[0].event_name == "Connexion"

    def test_audit_connexion_swallows_errors(self, db, backend):
        user = UtilisateurDjangoFactory()
        failing_usecase = MagicMock()
        failing_usecase.execute.side_effect = RuntimeError("boom")
        backend.container.log_utilisateur_connexion_usecase.override(failing_usecase)

        backend._audit_connexion(user)
