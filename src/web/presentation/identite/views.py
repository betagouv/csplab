from uuid import UUID

from authlib.integrations.base_client.errors import OAuthError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionInput,
)
from domain.identite.errors.identite_errors import UtilisateurNexistePas
from infrastructure.authentication.proconnect_backend import build_proconnect_logout_url
from infrastructure.authentication.proconnect_client import (
    fetch_userinfo_claims,
    oauth,
)
from infrastructure.di.identite.identite_factory import create_identite_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.identite.serializers import UtilisateurSerializer


class LoginView(auth_views.LoginView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()
        self.logger = self.container.logger_service()

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        self._audit_connexion(form.get_user())
        return response

    def _audit_connexion(self, user) -> None:
        # Auditing must never break the login flow (e.g. a non-UUID username on
        # a legacy/superuser account), so failures are swallowed and logged.
        try:
            usecase = self.container.log_utilisateur_connexion_usecase()
            usecase.execute(LogUtilisateurConnexionInput(utilisateur=user.to_entity()))
        except Exception as e:
            self.logger.error("Failed to audit login: %s", str(e))


class ProconnectLoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        redirect_uri = request.build_absolute_uri(
            reverse("identite:proconnect_callback")
        )
        return oauth.proconnect.authorize_redirect(
            request, redirect_uri, acr_values="eidas1"
        )


class ProconnectCallbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        try:
            token = oauth.proconnect.authorize_access_token(request)
            claims = fetch_userinfo_claims(token)
        except OAuthError:
            return self._login_failure(request)

        user = authenticate(request, proconnect_claims=claims)
        if user is None:
            return self._login_failure(request)

        login(
            request,
            user,
            backend="infrastructure.authentication.proconnect_backend.ProconnectBackend",
        )
        request.session["oidc_id_token"] = token.get("id_token")
        return redirect(settings.LOGIN_REDIRECT_URL)

    def _login_failure(self, request: HttpRequest) -> HttpResponseBase:
        messages.error(
            request,
            "Aucun compte ProConnect associé à cette adresse e-mail. "
            "Contactez votre administrateur.",
        )
        return redirect(settings.LOGIN_URL)


class ProconnectLogoutView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        id_token = request.session.get("oidc_id_token")
        logout(request)
        if id_token:
            return redirect(build_proconnect_logout_url(request, id_token))
        return redirect(settings.LOGOUT_REDIRECT_URL)


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
            username = request.user.username
            usecase = self.container.get_utilisateur_details_usecase()
            utilisateur = usecase.execute(username)
            return Response(UtilisateurSerializer(utilisateur).data)
        except UtilisateurNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            self.logger.error("Unexpected error in UserInfoView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
