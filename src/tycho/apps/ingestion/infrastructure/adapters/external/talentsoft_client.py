"""Mock TalentSoft client for testing purposes."""

import json

import requests

from apps.ingestion.config import TalentSoftConfig
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from core.services.logger_interface import ILogger


class TalentSoftClient(HttpClient):
    """Mock client for TalentSoft API - returns fake data for testing."""

    def __init__(
        self,
        config: TalentSoftConfig,
        logger_service: ILogger,
        timeout: int = 30,
    ):
        """Initialize with HTTP client."""
        super().__init__(timeout=timeout)
        self.config = config
        self.logger = logger_service.get_logger("TalentSoftClient")
        self.logger.info("Initializing TalentSoftClient (Mock)")

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Mock request that returns fake offer data."""
        self.logger.info(f"Mock TalentSoft API call: {method} {endpoint}")

        # TODO YOUNES
        # Create a mock response
        mock_response = requests.Response()
        mock_response.status_code = 200

        # Mock offer data
        mock_data = {
            "offers": [
                {
                    "id": "1",
                    "title": "Développeur Python Senior",
                    "profile": "Expérience en Python, Django, PostgreSQL",
                    "category": "A",
                    "region": "ILE_DE_FRANCE",
                    "department": "PARIS",
                    "limit_date": "2024-12-31T23:59:59Z",
                },
                {
                    "id": "2",
                    "title": "Data Scientist",
                    "profile": "Machine Learning, Python, SQL",
                    "category": "A",
                    "region": "AUVERGNE_RHONE_ALPES",
                    "department": "RHONE",
                    "limit_date": "2024-11-30T23:59:59Z",
                },
            ]
        }

        # Set the mock JSON data
        mock_response._content = json.dumps(mock_data).encode("utf-8")

        # Create a proper mock json method
        mock_response.json = lambda: mock_data  # type: ignore

        self.logger.info(f"Mock response: {len(mock_data['offers'])} offers")
        return mock_response
