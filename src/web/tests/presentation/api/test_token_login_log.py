import logging
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import (
    AuditLoginLogModel,
    AuditLoginLogQuerySet,
)
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


@pytest.fixture(name="logs")
def logs_fixture(caplog):
    caplog.set_level(logging.INFO, logger="identite")
    return caplog


class TestTokenLoginLog:
    def test_logs_successful_login_without_email(self, api_client, test_user, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": DEFAULT_PASSWORD},
            format="json",
            HTTP_X_REAL_IP="203.0.113.7",
            HTTP_X_FORWARDED_FOR="1.2.3.4",
        )

        assert response.status_code == status.HTTP_200_OK
        assert f"JWT login succeeded for user {test_user.pk}." in [
            r.getMessage() for r in logs.records
        ]
        assert test_user.email not in logs.text
        attempt = AuditLoginLogModel.objects.get()
        assert attempt.canal == Canal.JWT
        assert attempt.resultat == Resultat.SUCCES
        assert attempt.utilisateur_id == test_user.username
        assert attempt.ip_address == "203.0.113.7"

    def test_logs_failed_login_for_existing_user(self, api_client, test_user, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": "wrong"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert f"JWT login failed for user {test_user.pk}." in [
            r.getMessage() for r in logs.records
        ]
        assert test_user.email not in logs.text
        attempt = AuditLoginLogModel.objects.get()
        assert attempt.resultat == Resultat.ECHEC
        assert attempt.utilisateur_id == test_user.username

    def test_logs_failed_login_for_unknown_account(self, api_client, db, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": "nobody@example.com", "password": "wrong"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "JWT login failed for an unknown account." in [
            r.getMessage() for r in logs.records
        ]
        assert "nobody@example.com" not in logs.text
        attempt = AuditLoginLogModel.objects.get()
        assert attempt.resultat == Resultat.ECHEC
        assert attempt.utilisateur_id is None

    @pytest.mark.parametrize("real_ip", ["not-an-ip", ""], ids=["invalid", "empty"])
    def test_records_attempt_without_ip_when_client_ip_is_unusable(
        self, api_client, db, real_ip
    ):
        api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": "nobody@example.com", "password": "wrong"},
            format="json",
            HTTP_X_REAL_IP=real_ip,
            HTTP_X_FORWARDED_FOR="1.2.3.4",
        )

        attempt = AuditLoginLogModel.objects.get()
        assert attempt.resultat == Resultat.ECHEC
        assert attempt.ip_address is None

    def test_login_succeeds_when_the_audit_write_fails(
        self, api_client, test_user, logs
    ):
        with patch.object(
            AuditLoginLogQuerySet, "create", side_effect=RuntimeError("boom")
        ):
            response = api_client.post(
                reverse("api:token_obtain_pair"),
                {"email": test_user.email, "password": DEFAULT_PASSWORD},
                format="json",
            )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()
        assert not AuditLoginLogModel.objects.exists()
