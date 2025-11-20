"""Views for ingestion API endpoints."""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.application.usecases.load_documents import LoadDocumentsUsecase
from apps.ingestion.containers import IngestionContainer
from core.entities.document import DocumentType
from core.services.http_client import HttpClient
from core.services.logger import LoggerService

logger = logging.getLogger(__name__)


class LoadDocumentsView(APIView):
    """API endpoint to trigger document loading."""

    def post(self, request):
        """Trigger document loading process."""
        try:
            # Get document type from query params or default to CORPS
            document_type_str = request.query_params.get("type", "CORPS")

            try:
                document_type = DocumentType[document_type_str.upper()]
            except KeyError:
                error_msg = f"Invalid document type: {document_type_str}"
                return Response(
                    {"status": "error", "message": error_msg},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Setup container with dependencies
            container = IngestionContainer()
            container.in_memory_mode.override("external")

            logger_service = LoggerService()
            container.logger_service.override(logger_service)

            http_client = HttpClient()
            container.http_client.override(http_client)

            # Execute usecase
            usecase = LoadDocumentsUsecase(container)
            result = usecase.execute(document_type)

            created_count = result["created"]
            updated_count = result["updated"]
            message = f"{created_count} documents created, {updated_count} updated"
            return Response(
                {
                    "status": "success",
                    "document_type": document_type.value,
                    "created": result["created"],
                    "updated": result["updated"],
                    "message": message,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.exception("Failed to run document loading process.")
            error_message = f"Une erreur interne s'est produite: {str(e)}"
            return Response(
                {"status": "error", "message": error_message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
