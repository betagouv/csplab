from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.authentication.api_key_authentication import (
    ApiKeyAuthentication,
)
from infrastructure.di.ingestion.ingestion_factory import create_ingestion_container
from presentation.ingestion.serializers import (
    SourceSerializer,
)


@extend_schema(exclude=True)
class SourcesListView(APIView):
    authentication_classes = [ApiKeyAuthentication]

    def get(self, request):
        try:
            container = create_ingestion_container()
            sources = container.list_sources_usecase().execute()
            return Response(SourceSerializer(sources, many=True).data)
        except Exception:
            return Response(
                {"error": "Unexpected error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
