import logging

import pytest
from django.urls import reverse
from rest_framework import status

from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


@pytest.fixture(name="logs")
def logs_fixture(caplog):
    caplog.set_level(logging.INFO, logger="identite")
    return caplog


def _messages(logs):
    return [r.getMessage() for r in logs.records]


class TestTokenLoginLog:
    def test_logs_successful_login_without_email(self, api_client, test_user, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": DEFAULT_PASSWORD},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert _messages(logs) == [f"API login succeeded for user {test_user.pk}."]
        assert test_user.email not in logs.text

    def test_logs_failed_login_for_existing_user(self, api_client, test_user, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": "wrong"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert _messages(logs) == [f"API login failed for user {test_user.pk}."]
        assert test_user.email not in logs.text

    def test_logs_failed_login_for_unknown_account(self, api_client, db, logs):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": "nobody@example.com", "password": "wrong"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert _messages(logs) == ["API login failed for an unknown account."]
        assert "nobody@example.com" not in logs.text
