import logging
from typing import Any

from ddd.services.logger_interface import ILogger


class LoggerService(ILogger):
    def __init__(self, name: str = "web"):
        self.logger = logging.getLogger(name)

    def get_logger(self, module_name: str) -> logging.Logger:
        return logging.getLogger(f"web.{module_name}")

    def info(self, message: str, *args: Any) -> None:
        self.logger.info(message, *args)

    def debug(self, message: str, *args: Any) -> None:
        self.logger.debug(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        self.logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        self.logger.error(message, *args)
