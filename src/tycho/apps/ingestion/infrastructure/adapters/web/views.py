"""Views for ingestion API endpoints."""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.infrastructure.adapters.external.ingres_fetcher import (
    IngresCorpsRepository,
)

logger = logging.getLogger(__name__)


class CorpsETLView(APIView):
    """API endpoint pour déclencher l'ETL des corps."""

    def post(self, request):
        """Trigger corps ETL process."""
        try:
            sourcer = IngresCorpsRepository()
            count = sourcer.fetch_and_store_corps()

            return Response(
                {
                    "status": "success",
                    "corps_created": count,
                    "message": f"{count} nouveaux corps ingérés",
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception("Failed to run Corps ETL process.")
            return Response(
                {"status": "error", "message": "Une erreur interne s'est produite."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
