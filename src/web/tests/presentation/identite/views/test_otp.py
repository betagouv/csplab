import time
from unittest.mock import MagicMock

import pytest
from django.conf import settings
from django.contrib.messages import get_messages
from django.test import override_settings
from django.urls import reverse
from django_otp import DEVICE_ID_SESSION_KEY
from django_otp.oath import totp
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status

from infrastructure.authentication.proconnect_client import oauth
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD
from presentation.identite.otp_flow import PENDING_SESSION_KEY

LOGIN_URL = reverse("identite:login")
OTP_URL = reverse("identite:otp_verify")


@pytest.fixture(name="superuser")
def superuser_fixture(db):
    return UtilisateurDjangoFactory(is_superuser=True)


@pytest.fixture(name="device")
def device_fixture(superuser):
    return TOTPDevice.objects.create(user=superuser, confirmed=True)


def post_password(client, user, **extra):
    return client.post(
        LOGIN_URL,
        {"username": user.email, "password": DEFAULT_PASSWORD, **extra},
    )


def mock_proconnect(monkeypatch, email):
    monkeypatch.setattr(
        oauth.proconnect,
        "authorize_access_token",
        MagicMock(return_value={"id_token": "fake-id-token"}),
    )
    monkeypatch.setattr(
        "presentation.identite.views.fetch_userinfo_claims",
        MagicMock(return_value={"email": email}),
    )


class TestPasswordFlow:
    def test_superuser_is_sent_to_otp_step_without_being_logged_in(
        self, client, superuser, device
    ):
        response = post_password(client, superuser)

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == OTP_URL
        assert "_auth_user_id" not in client.session

    def test_valid_token_logs_in_and_verifies_the_session(
        self, client, superuser, device
    ):
        post_password(client, superuser)

        response = client.post(OTP_URL, {"otp_token": totp(device.bin_key)})

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session
        assert DEVICE_ID_SESSION_KEY in client.session
        assert PENDING_SESSION_KEY not in client.session

    def test_next_url_is_kept_after_otp(self, client, superuser, device):
        post_password(client, superuser, next="/ats/")

        response = client.post(OTP_URL, {"otp_token": totp(device.bin_key)})

        assert response.url == "/ats/"

    def test_external_next_url_is_ignored(self, client, superuser, device):
        post_password(client, superuser, next="https://evil.example/")

        response = client.post(OTP_URL, {"otp_token": totp(device.bin_key)})

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)

    def test_wrong_token_is_rejected(self, client, superuser, device):
        post_password(client, superuser)

        response = client.post(OTP_URL, {"otp_token": "000000"})

        assert response.status_code == status.HTTP_200_OK
        assert "_auth_user_id" not in client.session

    def test_malformed_token_is_rejected(self, client, superuser, device):
        post_password(client, superuser)

        response = client.post(OTP_URL, {"otp_token": "abc"})

        assert response.status_code == status.HTTP_200_OK
        assert "_auth_user_id" not in client.session

    def test_superuser_without_device_is_refused(self, client, superuser):
        response = post_password(client, superuser)

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == settings.LOGIN_URL
        assert "_auth_user_id" not in client.session
        assert PENDING_SESSION_KEY not in client.session
        assert any(
            "authentification à deux facteurs" in str(m)
            for m in get_messages(response.wsgi_request)
        )

    @override_settings(OTP_REQUIRED=False)
    def test_superuser_logs_in_directly_when_otp_is_disabled(self, client, superuser):
        response = post_password(client, superuser)

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session


class TestOtpStep:
    def test_without_pending_challenge_redirects_to_login(self, db, client):
        response = client.get(OTP_URL)

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == settings.LOGIN_URL

    def test_expired_challenge_redirects_to_login(self, client, superuser, device):
        post_password(client, superuser)
        session = client.session
        session[PENDING_SESSION_KEY]["started_at"] = time.time() - 3600
        session.save()

        response = client.post(OTP_URL, {"otp_token": totp(device.bin_key)})

        assert response.url == settings.LOGIN_URL
        assert "_auth_user_id" not in client.session


class TestProconnectFlow:
    def test_staff_is_sent_to_otp_step(self, db, client, monkeypatch):
        staff = UtilisateurDjangoFactory(is_staff=True)
        TOTPDevice.objects.create(user=staff, confirmed=True)
        mock_proconnect(monkeypatch, staff.email)

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.url == OTP_URL
        assert "_auth_user_id" not in client.session

    def test_valid_token_completes_login_and_keeps_oidc_id_token(
        self, db, client, monkeypatch
    ):
        staff = UtilisateurDjangoFactory(is_staff=True)
        device = TOTPDevice.objects.create(user=staff, confirmed=True)
        mock_proconnect(monkeypatch, staff.email)
        client.get(reverse("identite:proconnect_callback"))

        response = client.post(OTP_URL, {"otp_token": totp(device.bin_key)})

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session
        assert client.session["oidc_id_token"] == "fake-id-token"  # noqa: S105

    def test_staff_without_device_is_refused(self, db, client, monkeypatch):
        staff = UtilisateurDjangoFactory(is_staff=True)
        mock_proconnect(monkeypatch, staff.email)

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.url == settings.LOGIN_URL
        assert "_auth_user_id" not in client.session

    def test_non_staff_agent_logs_in_directly(self, db, client, monkeypatch):
        agent = UtilisateurDjangoFactory()
        mock_proconnect(monkeypatch, agent.email)

        response = client.get(reverse("identite:proconnect_callback"))

        assert response.url == reverse(settings.LOGIN_REDIRECT_URL)
        assert "_auth_user_id" in client.session
