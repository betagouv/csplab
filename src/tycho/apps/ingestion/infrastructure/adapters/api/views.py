"""Views for ingestion API endpoints."""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.external.logger import LoggerService
from core.entities.document import DocumentType
from core.errors.domain_errors import InvalidDocumentTypeError

logger = logging.getLogger(__name__)


class LoadDocumentsView(APIView):
    """API endpoint to trigger document loading."""

    def post(self, request):
        """Trigger document loading process."""
        document_type_str = request.data.get("type", "CORPS")

        try:
            document_type = DocumentType[document_type_str.upper()]
        except KeyError:
            raise InvalidDocumentTypeError(document_type_str) from None

        # Setup container with dependencies
        container = IngestionContainer()
        container.in_memory_mode.override("external")

        logger_service = LoggerService()
        container.logger_service.override(logger_service)

        http_client = HttpClient()
        container.http_client.override(http_client)

        # Execute usecase - exceptions handled by global exception handler
        usecase = container.load_documents_usecase()
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
