from unittest.mock import patch

from sentry_sdk.integrations.celery import CeleryIntegration

from api.config import Settings
from infrastructure.observability.sentry import (
    init_sentry,
    scrub_dict,
    strip_sentry_sensitive_data,
)

DSN = "https://key@o123.ingest.sentry.io/123"


class TestScrubDict:
    def test_filters_sensitive_keys(self):
        data = {"password": "secret", "token": "abc", "name": "Alice"}
        result = scrub_dict(data)
        assert result["password"] == "[Filtered]"
        assert result["token"] == "[Filtered]"
        assert result["name"] == "Alice"

    def test_filtering_is_case_insensitive(self):
        data = {"Authorization": "Bearer token", "Content-Type": "application/json"}
        result = scrub_dict(data)
        assert result["Authorization"] == "[Filtered]"
        assert result["Content-Type"] == "application/json"

    def test_empty_dict(self):
        assert scrub_dict({}) == {}

    def test_no_sensitive_keys(self):
        data = {"foo": "bar", "baz": 42}
        assert scrub_dict(data) == {"foo": "bar", "baz": 42}


class TestStripSentrySensitiveData:
    def test_scrubs_request_data(self):
        event = {"request": {"data": {"password": "secret", "username": "alice"}}}
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["data"]["password"] == "[Filtered]"
        assert result["request"]["data"]["username"] == "[Filtered]"

    def test_scrubs_request_headers(self):
        event = {
            "request": {
                "headers": {
                    "Authorization": "Bearer token",
                    "Accept": "application/json",
                }
            }
        }
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["headers"]["Authorization"] == "[Filtered]"
        assert result["request"]["headers"]["Accept"] == "application/json"

    def test_ignores_non_dict_request_data(self):
        event = {"request": {"data": "raw-body-string"}}
        result = strip_sentry_sensitive_data(event, {})
        assert result["request"]["data"] == "raw-body-string"

    def test_handles_event_without_request(self):
        event = {"level": "error"}
        result = strip_sentry_sensitive_data(event, {})
        assert result == {"level": "error"}


@patch("infrastructure.observability.sentry.sentry_sdk.init")
class TestInitSentry:
    def test_does_nothing_without_dsn(self, mock_sentry_init):
        init_sentry(Settings(sentry_dsn=None), tracing=True)

        mock_sentry_init.assert_not_called()

    def test_filters_sensitive_data_and_adds_given_integrations(self, mock_sentry_init):
        celery_integration = CeleryIntegration()

        init_sentry(Settings(sentry_dsn=DSN), [celery_integration], tracing=False)

        kwargs = mock_sentry_init.call_args.kwargs
        assert kwargs["dsn"] == DSN
        assert kwargs["send_default_pii"] is False
        assert kwargs["before_send"] is strip_sentry_sensitive_data
        assert celery_integration in kwargs["integrations"]

    def test_enables_tracing_with_configured_sample_rates(self, mock_sentry_init):
        settings = Settings(
            sentry_dsn=DSN,
            sentry_traces_sample_rate=0.2,
            sentry_profiles_sample_rate=0.3,
        )

        init_sentry(settings, tracing=True)

        kwargs = mock_sentry_init.call_args.kwargs
        assert kwargs["traces_sample_rate"] == 0.2
        assert kwargs["profiles_sample_rate"] == 0.3
        assert kwargs["before_send_transaction"] is strip_sentry_sensitive_data

    def test_disables_tracing_for_scripts(self, mock_sentry_init):
        init_sentry(Settings(sentry_dsn=DSN), tracing=False)

        kwargs = mock_sentry_init.call_args.kwargs
        assert kwargs["traces_sample_rate"] is None
        assert kwargs["profiles_sample_rate"] is None
        assert kwargs["before_send_transaction"] is None
