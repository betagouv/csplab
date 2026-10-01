import logging

import pytest
from django.test import override_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory

from infrastructure.authentication.api_key_authentication import ApiKeyAuthentication


@pytest.fixture(name="logs")
def logs_fixture(caplog):
    caplog.set_level(logging.INFO, logger="identite")
    return caplog


def _request(key: str, **extra):
    return APIRequestFactory().get("/", HTTP_AUTHORIZATION=f"Api-Key {key}", **extra)


class TestApiKeyAuthenticationLog:
    def test_logs_invalid_key_without_the_key(self, logs):
        with pytest.raises(AuthenticationFailed):
            ApiKeyAuthentication().authenticate(
                _request("secret-wrong-key", REMOTE_ADDR="10.0.0.1")
            )

        assert [r.getMessage() for r in logs.records] == [
            "Ingestion API key rejected (invalid key) from 10.0.0.1."
        ]
        assert "secret-wrong-key" not in logs.text

    @override_settings(
        INGESTION_API_KEY="good-key", INGESTION_API_KEY_ALLOWED_IP_RANGES=["10.0.0.0/8"]
    )
    def test_logs_ip_not_allowed(self, logs):
        with pytest.raises(AuthenticationFailed):
            ApiKeyAuthentication().authenticate(
                _request("good-key", REMOTE_ADDR="192.168.1.1")
            )

        assert [r.getMessage() for r in logs.records] == [
            "Ingestion API key rejected (IP not allowed) from 192.168.1.1."
        ]
        assert "good-key" not in logs.text

    @override_settings(INGESTION_API_KEY="good-key")
    def test_valid_key_logs_nothing(self, logs):
        ApiKeyAuthentication().authenticate(_request("good-key"))

        assert not logs.records
