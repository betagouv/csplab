"""Corps sourcing service for INGRES API integration."""

import logging
import traceback

from ingestion.models import RawCorps

from .piste_client import PisteClient

logger = logging.getLogger(__name__)


class CorpsSourcer:
    """Service for sourcing corps data from INGRES API."""

    def __init__(self):
        """Initialize CorpsSourcer with PisteClient."""
        self.client = PisteClient()

    def fetch_and_store_corps(self) -> int:
        """Fetch corps data from INGRES API and store in database."""
        try:
            logger.info("Starting corps sourcing")
            response = self.client.request(
                "GET", "CORPS", params={"enVigueur": "true", "full": "true"}
            )
            logger.info(f"Response status: {response.status_code}")
            documents = response.json()["items"]
            logger.info(f"Found {len(documents)} documents")

            created_count = 0
            for doc in documents:
                # Upsert basé sur un identifiant unique
                raw_corps, created = RawCorps.objects.update_or_create(
                    ingres_id=doc.get("id"),  # Clé unique
                    defaults={"raw_data": doc},
                )
                if created:
                    created_count += 1

            logger.info(
                f"Corps sourcing completed: {created_count} new records created"
            )
            return created_count
        except Exception as e:
            logger.error(f"Error during corps sourcing: {e}")
            logger.error(traceback.format_exc())
            raise
