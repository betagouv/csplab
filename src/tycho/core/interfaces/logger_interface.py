"""Logger service interface definitions."""

import logging
from typing import Protocol


class ILoggerService(Protocol):
    """Interface for logger service."""

    def get_logger(self, module_name: str) -> logging.Logger:
        """Get logger for specific module.

        Args:
            module_name: Module name for logger

        Returns:
            Configured logger instance
        """
        ...
