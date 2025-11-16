"""Logger service implementation."""

import logging

from core.interfaces.logger_interface import ILoggerService


class LoggerService(ILoggerService):
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
