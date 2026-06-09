from uuid import UUID

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.di.identite.identite_factory import create_identite_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.identite.serializers import UtilisateurSerializer


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "registration/profile.html"


@extend_schema(
    summary="Detail de l'utilisateur connecté",
    tags=["utilisateurs"],
    responses={
        200: UtilisateurSerializer,
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class UtilisateurDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UtilisateurSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()
        self.logger = self.container.logger_service()

    def get(self, request):
        try:
            entity_id = UUID(request.user.username)
            usecase = self.container.get_utilisateur_details_usecase()
            utilisateur = usecase.execute(entity_id)
            return Response(UtilisateurSerializer(utilisateur).data)
        except Exception as e:
            self.logger.error("Unexpected error in UserInfoView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
