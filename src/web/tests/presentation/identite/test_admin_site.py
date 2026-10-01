import logging
from unittest.mock import MagicMock

import pytest
from django.http import HttpResponse, HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

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
    def test_logs_successful_login(self, logs):
        user = MagicMock(pk="abc", is_authenticated=True)
        Site.response = HttpResponseRedirect(reverse("admin:index"))

        Site().login(_post(user=user, username="x@example.com"))

        assert [r.getMessage() for r in logs.records] == [
            "Admin login succeeded for user abc."
        ]

    def test_logs_failed_login_for_existing_user_without_email(self, db, logs):
        user = UtilisateurDjangoFactory()
        Site.response = HttpResponse()

        Site().login(_post(username=user.email))

        assert [r.getMessage() for r in logs.records] == [
            f"Admin login failed for user {user.pk}."
        ]
        assert user.email not in logs.text

    def test_logs_failed_login_for_unknown_account(self, db, logs):
        Site.response = HttpResponse()

        Site().login(_post(username="unknown@example.com"))

        assert [r.getMessage() for r in logs.records] == [
            "Admin login failed for an unknown account."
        ]

    def test_ignores_otp_challenge_request(self, logs):
        Site.response = HttpResponse()

        Site().login(_post(username="x@example.com", otp_challenge="1"))

        assert not logs.records

    def test_ignores_get_request(self, logs):
        Site.response = HttpResponse()

        Site().login(RequestFactory().get(reverse("admin:login")))

        assert not logs.records
