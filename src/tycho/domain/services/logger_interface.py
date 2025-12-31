"""Logger service interface definitions."""

import logging
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ILogger(Protocol):
    """Interface for logger service."""

    def get_logger(self, module_name: str) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Module name for logger

        Returns:
            Configured logger instance
        """
        ...

    def info(self, message: str, *args: Any) -> None:
        """Log info message with automatic context capture."""
        ...

    def debug(self, message: str, *args: Any) -> None:
        """Log debug message with automatic context capture."""
        ...

    def warning(self, message: str, *args: Any) -> None:
        """Log warning message with automatic context capture."""
        ...

    def error(self, message: str, *args: Any) -> None:
        """Log error message with automatic context capture."""
        ...
