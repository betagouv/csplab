"""Logger service implementation."""

import logging
from typing import Any

from core.interfaces.logger_interface import ILogger


class LoggerService(ILogger):
    """Centralized logger service."""

    def __init__(self, name: str = "tycho"):
        """Initialize logger service.

        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)

    def get_logger(self, module_name: str) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Module name for logger

        Returns:
            Configured logger instance
        """
        return logging.getLogger(f"tycho.{module_name}")

    def info(self, message: str, *args: Any) -> None:
        """Log info message."""
        self.logger.info(message, *args)

    def debug(self, message: str, *args: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        """Log error message."""
        self.logger.error(message, *args)
