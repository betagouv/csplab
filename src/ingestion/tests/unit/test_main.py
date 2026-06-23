import logging
import sys
from unittest.mock import patch

from api.main import _PlaintextFormatter, create_app


class TestPlaintextFormatter:
    def _make_record(self, msg="hello", level=logging.INFO, name="test", **extras):
        record = logging.LogRecord(name, level, "", 0, msg, (), None)
        for k, v in extras.items():
            setattr(record, k, v)
        return record

    def test_formats_basic_message(self):
        formatter = _PlaintextFormatter()
        record = self._make_record("hello world")
        assert formatter.format(record) == "INFO test: hello world"

    def test_includes_extra_fields(self):
        formatter = _PlaintextFormatter()
        record = self._make_record("hello", client_id="abc123")
        result = formatter.format(record)
        assert "client_id=abc123" in result

    def test_no_extra_section_when_no_extras(self):
        formatter = _PlaintextFormatter()
        record = self._make_record("hello")
        result = formatter.format(record)
        # No trailing space or extra key=value pairs
        assert result == "INFO test: hello"

    def test_includes_exception_info(self):
        formatter = _PlaintextFormatter()
        try:
            raise ValueError("something went wrong")
        except ValueError:
            exc_info = sys.exc_info()
        record = self._make_record("error occurred", level=logging.ERROR)
        record.exc_info = exc_info
        result = formatter.format(record)
        assert "ValueError: something went wrong" in result


class TestCreateApp:
    @patch("api._sentry.sentry_sdk.init")
    def test_create_app_initializes_sentry_when_dsn_is_set(
        self, mock_sentry_init, monkeypatch
    ):
        monkeypatch.setenv("TESTING", "true")
        monkeypatch.setenv("SENTRY_DSN", "https://key@o123.ingest.sentry.io/123")

        create_app()

        mock_sentry_init.assert_called_once()

    @patch("api._sentry.sentry_sdk.init")
    def test_create_app_skips_sentry_when_no_dsn(self, mock_sentry_init, monkeypatch):
        monkeypatch.setenv("TESTING", "true")
        monkeypatch.delenv("SENTRY_DSN", raising=False)

        create_app()

        mock_sentry_init.assert_not_called()
