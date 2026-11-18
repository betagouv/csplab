import logging
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

_RECORD_ATTRS = frozenset(logging.LogRecord("", 0, "", 0, "", (), None).__dict__) | {
    "message",
    "asctime",
    "exc_text",
}

_log_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "log_context", default=None
)


@contextmanager
def log_context(context: dict[str, Any]) -> Iterator[None]:
    token = _log_context.set(context)
    try:
        yield
    finally:
        _log_context.reset(token)


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        for key, value in (_log_context.get() or {}).items():
            if not hasattr(record, key):
                setattr(record, key, value)
        return True


class PlaintextFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        extras = {k: v for k, v in record.__dict__.items() if k not in _RECORD_ATTRS}
        if record.name.startswith("celery."):
            extras.pop("data", None)
        pairs = " ".join(f"{k}={v}" for k, v in extras.items())
        extra_str = f" {pairs}" if pairs else ""
        line = f"{record.levelname} {record.name}: {record.getMessage()}{extra_str}"
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(PlaintextFormatter())
    handler.addFilter(ContextFilter())
    logging.basicConfig(level=level.upper(), handlers=[handler], force=True)
