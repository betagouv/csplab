"""Views for ingestion API endpoints."""

from typing import cast

import environ
from pydantic import HttpUrl
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.config import IngestionConfig, PisteConfig
from apps.ingestion.containers import IngestionContainer
from apps.ingestion.infrastructure.adapters.external.http_client import HttpClient
from apps.ingestion.infrastructure.adapters.external.logger import LoggerService
from core.entities.document import DocumentType
from core.errors.document_error import InvalidDocumentTypeError


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

        # Create configuration from environment variables
        env = environ.Env()
        piste_config = PisteConfig(
            oauth_base_url=cast(HttpUrl, env.str("TYCHO_PISTE_OAUTH_BASE_URL")),
            ingres_base_url=cast(HttpUrl, env.str("TYCHO_INGRES_BASE_URL")),
            client_id=cast(str, env.str("TYCHO_INGRES_CLIENT_ID")),
            client_secret=cast(str, env.str("TYCHO_INGRES_CLIENT_SECRET")),
        )
        logger = logger_service.get_logger("INFRASTRUCTURE")
        logger.info(piste_config.oauth_base_url)
        logger.info(piste_config.ingres_base_url)
        config = IngestionConfig(piste_config)
        container.config.override(config)

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
