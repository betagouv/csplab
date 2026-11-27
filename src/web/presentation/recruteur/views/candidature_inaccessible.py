from rest_framework import status
from rest_framework.response import Response

from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from presentation.api.serializers import GenericErrorSerializer


def candidature_inaccessible_response() -> Response:
    return Response(
        GenericErrorSerializer({"error": CandidatureInaccessible.MESSAGE}).data,
        status=status.HTTP_404_NOT_FOUND,
    )
