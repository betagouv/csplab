import logging
import sys

import pytest
from celery.signals import setup_logging

from infrastructure.observability.log_config import (
    PlaintextFormatter,
    configure_logging,
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


@pytest.mark.usefixtures("restore_root_logger")
def test_worker_logging_uses_plaintext_formatter():
    import infrastructure.celery_app  # noqa: F401, PLC0415

    setup_logging.send(sender=None)

    assert isinstance(logging.getLogger().handlers[0].formatter, PlaintextFormatter)
