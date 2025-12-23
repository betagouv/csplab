"""TalentSoft client"""

from __future__ import annotations

import requests

from apps.ingestion.config import TalentSoftConfig
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from core.services.logger_interface import ILogger

from .talentsoft.client import TalentSoftHttpClient


class TalentSoftClient(HttpClient):
    """
    Façade compat.

    Toute la logique HTTP / token / mapping est dans TalentSoftHttpClient.
    """

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        timeout: int = 30,
    ):
        super().__init__(timeout=timeout)
        self.config = config
        self.logger = logger_service.get_logger("TalentSoftClient")
        self._delegate = TalentSoftHttpClient(
            config=config,
            logger_service=logger_service,
            timeout=timeout,
        )
        self.logger.info("Initializing TalentSoftClient (Facade -> Real)")

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Délègue la requête au vrai client TalentSoft."""
        return self._delegate.request(method=method, endpoint=endpoint, **kwargs)
