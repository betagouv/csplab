import logging
from unittest.mock import MagicMock

import pytest
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from presentation.identite.admin_site import LoginLoggingAdminSiteMixin


class FakeSite:
    response: HttpResponse = HttpResponse()

    def login(self, request, extra_context=None):
        return self.response


class Site(LoginLoggingAdminSiteMixin, FakeSite):
    pass


@pytest.fixture(name="logs")
def logs_fixture(caplog):
    caplog.set_level(logging.INFO, logger="identite")
    return caplog


def _post(user=None, **data):
    request = RequestFactory().post(reverse("admin:login"), data)
    request.user = user or MagicMock(is_authenticated=False)
    return request


class TestLoginLoggingAdminSite:
    def test_logs_successful_login(self, db, logs):
        user = UtilisateurDjangoFactory()
        Site.response = HttpResponseRedirect(reverse("admin:index"))

        Site().login(_post(user=user, username="x@example.com"))

        assert [r.getMessage() for r in logs.records] == [
            f"ADMIN login succeeded for user {user.pk}."
        ]
        attempt = AuditLoginLogModel.objects.get()
        assert attempt.canal == Canal.ADMIN
        assert attempt.resultat == Resultat.SUCCES
        assert attempt.utilisateur_id == user.username

    def test_logs_failed_login_for_existing_user_without_email(self, db, logs):
        user = UtilisateurDjangoFactory()
        Site.response = HttpResponse()

        Site().login(_post(username=user.email))

        assert [r.getMessage() for r in logs.records] == [
            f"ADMIN login failed for user {user.pk}."
        ]
        attempt = AuditLoginLogModel.objects.get()
        assert attempt.resultat == Resultat.ECHEC
        assert attempt.utilisateur_id == user.username
        assert user.email not in logs.text

    def test_logs_failed_login_for_unknown_account(self, db, logs):
        Site.response = HttpResponse()

        Site().login(_post(username="unknown@example.com"))

        assert [r.getMessage() for r in logs.records] == [
            "ADMIN login failed for an unknown account."
        ]
        assert AuditLoginLogModel.objects.get().utilisateur_id is None

    def test_ignores_otp_challenge_request(self, db, logs):
        Site.response = HttpResponse()

        Site().login(_post(username="x@example.com", otp_challenge="1"))

        assert not logs.records
        assert not AuditLoginLogModel.objects.exists()

    def test_ignores_get_request(self, db, logs):
        Site.response = HttpResponse()

        Site().login(RequestFactory().get(reverse("admin:login")))

        assert not logs.records
        assert not AuditLoginLogModel.objects.exists()

    def test_records_the_client_ip(self, db, logs):
        Site.response = HttpResponse()
        request = _post(username="unknown@example.com")
        request.META["HTTP_X_REAL_IP"] = "203.0.113.7"
        request.META["HTTP_X_FORWARDED_FOR"] = "1.2.3.4"

        Site().login(request)

        assert AuditLoginLogModel.objects.get().ip_address == "203.0.113.7"

    def test_records_the_attempt_without_ip_when_client_ip_is_invalid(self, db, logs):
        Site.response = HttpResponse()
        request = _post(username="unknown@example.com")
        request.META["HTTP_X_REAL_IP"] = "not-an-ip"

        Site().login(request)

        assert AuditLoginLogModel.objects.get().ip_address is None
