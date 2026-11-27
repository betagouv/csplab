from rest_framework import status
from rest_framework.response import Response

from presentation.api.serializers import GenericErrorSerializer

CANDIDATURE_INACCESSIBLE_MESSAGE = "Cette candidature n'est pas accessible."


def candidature_inaccessible_response() -> Response:
    return Response(
        GenericErrorSerializer({"error": CANDIDATURE_INACCESSIBLE_MESSAGE}).data,
        status=status.HTTP_404_NOT_FOUND,
    )
