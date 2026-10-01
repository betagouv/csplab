from unittest.mock import MagicMock

import pytest
from django.test import RequestFactory

from infrastructure.authentication.proconnect_backend import ProconnectBackend
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


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

    def test_authenticate_logs_the_successful_login(self, db, backend):
        user = UtilisateurDjangoFactory()
        backend.logger = MagicMock()

        backend.authenticate(None, proconnect_claims={"email": user.email})

        backend.logger.info.assert_called_once_with(
            "User %s logged in through ProConnect.", user.pk
        )

    def test_authenticate_returns_none_for_unknown_email(self, db, backend):
        backend.logger = MagicMock()

        authenticated = backend.authenticate(
            None, proconnect_claims={"email": "unknown@example.com"}
        )

        assert authenticated is None
        backend.logger.warning.assert_called_once()
        backend.logger.info.assert_not_called()

    def test_authenticate_returns_none_without_claims(self, db, backend):
        assert backend.authenticate(None, proconnect_claims=None) is None
        assert backend.authenticate(None, proconnect_claims={}) is None

    def test_authenticate_ignores_calls_that_are_not_proconnect(self, db, backend):
        backend.logger = MagicMock()

        assert backend.authenticate(None, proconnect_claims=None) is None

        backend.logger.warning.assert_not_called()

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

    def test_authenticate_records_the_successful_login(self, db, backend):
        user = UtilisateurDjangoFactory()

        backend.authenticate(None, proconnect_claims={"email": user.email})

        attempt = AuditLoginLogModel.objects.get()
        assert attempt.canal == Canal.PROCONNECT
        assert attempt.resultat == Resultat.SUCCES
        assert attempt.utilisateur_id == user.username

    def test_authenticate_records_the_failed_login(self, db, backend):
        claims_rejetes = [{"email": "unknown@example.com"}, {}]

        for claims in claims_rejetes:
            backend.authenticate(None, proconnect_claims=claims)

        attempts = list(AuditLoginLogModel.objects.all())
        assert len(attempts) == len(claims_rejetes)
        assert all(
            a.resultat == Resultat.ECHEC and a.utilisateur_id is None for a in attempts
        )

    def test_authenticate_records_the_client_ip(self, db, backend):
        user = UtilisateurDjangoFactory()
        request = RequestFactory().get(
            "/", HTTP_X_REAL_IP="203.0.113.7", HTTP_X_FORWARDED_FOR="1.2.3.4"
        )

        backend.authenticate(request, proconnect_claims={"email": user.email})

        assert AuditLoginLogModel.objects.get().ip_address == "203.0.113.7"

    def test_authenticate_records_the_attempt_without_ip_when_client_ip_is_invalid(
        self, db, backend
    ):
        request = RequestFactory().get("/", HTTP_X_REAL_IP="not-an-ip")

        backend.authenticate(request, proconnect_claims={"email": "nobody@example.com"})

        attempt = AuditLoginLogModel.objects.get()
        assert attempt.resultat == Resultat.ECHEC
        assert attempt.ip_address is None
