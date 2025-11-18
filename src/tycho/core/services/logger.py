"""Logger service implementation."""

import inspect
import logging

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
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back if frame else None
            if caller_frame and "self" in caller_frame.f_locals:
                class_name = caller_frame.f_locals["self"].__class__.__name__
                return logging.getLogger(f"tycho.{module_name}.{class_name}")
            return logging.getLogger(f"tycho.{module_name}")
        finally:
            del frame
