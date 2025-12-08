"""Views for ingestion API endpoints."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.container_singleton import IngestionContainerSingleton
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

        container = IngestionContainerSingleton.get_container()

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
