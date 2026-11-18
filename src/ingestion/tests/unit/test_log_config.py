import logging
import sys

import pytest
from celery.signals import setup_logging

from infrastructure.observability.log_config import (
    ContextFilter,
    PlaintextFormatter,
    configure_logging,
    log_context,
)


class TestPlaintextFormatter:
    def _make_record(self, msg="hello", level=logging.INFO, name="test", **extras):
        record = logging.LogRecord(name, level, "", 0, msg, (), None)
        for k, v in extras.items():
            setattr(record, k, v)
        return record

    def test_formats_basic_message(self):
        formatter = PlaintextFormatter()
        record = self._make_record("hello world")
        assert formatter.format(record) == "INFO test: hello world"

    def test_includes_extra_fields(self):
        formatter = PlaintextFormatter()
        record = self._make_record("hello", client_id="abc123")
        result = formatter.format(record)
        assert "client_id=abc123" in result

    def test_no_extra_section_when_no_extras(self):
        formatter = PlaintextFormatter()
        record = self._make_record("hello")
        result = formatter.format(record)
        # No trailing space or extra key=value pairs
        assert result == "INFO test: hello"

    def test_includes_exception_info(self):
        formatter = PlaintextFormatter()
        try:
            raise ValueError("something went wrong")
        except ValueError:
            exc_info = sys.exc_info()
        record = self._make_record("error occurred", level=logging.ERROR)
        record.exc_info = exc_info
        result = formatter.format(record)
        assert "ValueError: something went wrong" in result

    def test_omits_data_field_of_celery_records(self):
        formatter = PlaintextFormatter()
        record = self._make_record(
            "Task failed", name="celery.app.trace", data={"traceback": "..."}
        )
        assert formatter.format(record) == "INFO celery.app.trace: Task failed"

    def test_keeps_data_field_of_other_records(self):
        formatter = PlaintextFormatter()
        record = self._make_record("hello", data="abc")
        assert "data=abc" in formatter.format(record)


class TestContextFilter:
    def _make_record(self, **extras):
        record = logging.LogRecord("test", logging.INFO, "", 0, "hello", (), None)
        for k, v in extras.items():
            setattr(record, k, v)
        return record

    def test_adds_context_to_record(self):
        record = self._make_record()
        with log_context({"webhook_id": "abc"}):
            ContextFilter().filter(record)
        assert record.webhook_id == "abc"

    def test_keeps_record_own_values(self):
        record = self._make_record(webhook_id="own")
        with log_context({"webhook_id": "abc"}):
            ContextFilter().filter(record)
        assert record.webhook_id == "own"

    def test_no_context_outside_block(self):
        with log_context({"webhook_id": "abc"}):
            pass
        record = self._make_record()
        ContextFilter().filter(record)
        assert not hasattr(record, "webhook_id")


@pytest.fixture
def restore_root_logger():
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    yield
    root.handlers[:] = handlers
    root.setLevel(level)


@pytest.mark.usefixtures("restore_root_logger")
def test_configure_logging_installs_plaintext_formatter_on_root():
    configure_logging("warning")

    root = logging.getLogger()
    assert root.level == logging.WARNING
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0].formatter, PlaintextFormatter)
    assert any(isinstance(f, ContextFilter) for f in root.handlers[0].filters)


@pytest.mark.usefixtures("restore_root_logger")
def test_worker_logging_uses_plaintext_formatter():
    import infrastructure.celery_app  # noqa: F401, PLC0415

    setup_logging.send(sender=None)

    assert isinstance(logging.getLogger().handlers[0].formatter, PlaintextFormatter)
