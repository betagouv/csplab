from unittest.mock import patch

from api.main import create_app


class TestCreateApp:
    @patch("infrastructure.observability.sentry.sentry_sdk.init")
    def test_create_app_initializes_sentry_when_dsn_is_set(
        self, mock_sentry_init, monkeypatch
    ):
        monkeypatch.setenv("TESTING", "true")
        monkeypatch.setenv("SENTRY_DSN", "https://key@o123.ingest.sentry.io/123")

        create_app()

        mock_sentry_init.assert_called_once()

    @patch("infrastructure.observability.sentry.sentry_sdk.init")
    def test_create_app_skips_sentry_when_no_dsn(self, mock_sentry_init, monkeypatch):
        monkeypatch.setenv("TESTING", "true")
        monkeypatch.delenv("SENTRY_DSN", raising=False)

        create_app()

        mock_sentry_init.assert_not_called()
