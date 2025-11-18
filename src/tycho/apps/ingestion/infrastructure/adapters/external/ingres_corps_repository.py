"""Corps sourcing service for INGRES API integration."""

import logging
import traceback
from typing import Optional

from apps.ingestion.infrastructure.adapters.persistence.models import IngresCorps
from core.interfaces.http_client_interface import IHttpClient
from core.interfaces.logger_interface import ILogger


class IngresCorpsRepository:
    """Service for sourcing corps data from INGRES API."""

    def __init__(self, client: IHttpClient, logger_service: Optional[ILogger] = None):
        """Initialize CorpsSourcer with dependencies.

        Args:
            client: PISTE API client
            logger_service: Logger service for centralized logging
        """
        self.client = client
        self.logger = (
            logger_service.get_logger("corps_sourcer")
            if logger_service
            else logging.getLogger(__name__)
        )

    def fetch_and_store_corps(self) -> int:
        """Fetch corps data from INGRES API and store in database."""
        try:
            self.logger.info("Starting corps sourcing")
            response = self.client.request(
                "GET", "CORPS", params={"enVigueur": "true", "full": "true"}
            )
            self.logger.info(f"Response status: {response.status_code}")
            documents = response.json()["items"]
            self.logger.info(f"Found {len(documents)} documents")

            created_count = 0
            for doc in documents:
                # Upsert basé sur un identifiant unique
                raw_corps, created = IngresCorps.objects.update_or_create(  # type: ignore[attr-defined]
                    ingres_id=doc.get("id"),  # Clé unique
                    defaults={"raw_data": doc},
                )
                if created:
                    created_count += 1

            self.logger.info(
                f"Corps sourcing completed: {created_count} new records created"
            )
            return created_count
        except Exception as e:
            self.logger.error(f"Error during corps sourcing: {e}")
            self.logger.error(traceback.format_exc())
            raise
