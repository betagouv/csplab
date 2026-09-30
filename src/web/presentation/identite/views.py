from authlib.integrations.base_client.errors import OAuthError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import FormView, TemplateView
from django_otp import login as otp_login
from django_otp import match_token
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
from presentation.identite.forms import OtpTokenForm, SuperuserAuthenticationForm
from presentation.identite.otp_flow import (
    NO_DEVICE_MESSAGE,
    clear_pending,
    get_pending,
    has_confirmed_device,
    load_pending_user,
    requires_otp,
    start_challenge,
)
from presentation.identite.serializers import UtilisateurSerializer


class LoginAuditMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()
        self.logger = self.container.logger_service()

    def _audit_connexion(self, user) -> None:
        # Auditing must never break the login flow (e.g. a non-UUID username on
        # a legacy/superuser account), so failures are swallowed and logged.
        try:
            details_usecase = self.container.get_utilisateur_details_usecase()
            utilisateur = details_usecase.execute(user.username)
            usecase = self.container.log_utilisateur_connexion_usecase()
            usecase.execute(LogUtilisateurConnexionInput(utilisateur=utilisateur))
        except Exception as e:
            self.logger.error("Failed to audit login: %s", str(e))


class LoginView(LoginAuditMixin, auth_views.LoginView):
    form_class = SuperuserAuthenticationForm

    def form_valid(self, form) -> HttpResponse:
        user = form.get_user()
        if requires_otp(user):
            if not has_confirmed_device(user):
                messages.error(self.request, NO_DEVICE_MESSAGE)
                return redirect(settings.LOGIN_URL)
            start_challenge(
                self.request,
                user,
                user.backend,
                next_url=self.get_redirect_url(),
                audit=True,
            )
            return redirect("identite:otp_verify")
        response = super().form_valid(form)
        self._audit_connexion(user)
        return response


class OtpVerifyView(LoginAuditMixin, FormView):
    form_class = OtpTokenForm
    template_name = "registration/otp.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        self.pending = get_pending(request)
        self.user = load_pending_user(self.pending) if self.pending else None
        if self.user is None:
            clear_pending(request)
            return redirect(settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form) -> HttpResponse:
        device = match_token(self.user, form.cleaned_data["otp_token"])
        if device is None:
            form.add_error("otp_token", "Code invalide ou expiré.")
            return self.form_invalid(form)

        pending = self.pending
        clear_pending(self.request)
        login(self.request, self.user, backend=pending["backend"])
        otp_login(self.request, device)
        if pending["oidc_id_token"]:
            self.request.session["oidc_id_token"] = pending["oidc_id_token"]
        if pending["audit"]:
            self._audit_connexion(self.user)
        return redirect(self._success_url(pending["next_url"]))

    def _success_url(self, next_url: str) -> str:
        is_safe = url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        )
        return next_url if next_url and is_safe else settings.LOGIN_REDIRECT_URL


class ProconnectLoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        if not settings.PROCONNECT_LOGIN_ENABLED:
            raise Http404
        redirect_uri = request.build_absolute_uri(
            reverse("identite:proconnect_callback")
        )
        return oauth.proconnect.authorize_redirect(
            request, redirect_uri, acr_values="eidas1"
        )


class ProconnectCallbackView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:
        if not settings.PROCONNECT_LOGIN_ENABLED:
            raise Http404
        try:
            token = oauth.proconnect.authorize_access_token(request)
            claims = fetch_userinfo_claims(token)
        except OAuthError:
            return self._login_failure(request)

        user = authenticate(request, proconnect_claims=claims)
        if user is None:
            return self._login_failure(request)

        if requires_otp(user):
            if not has_confirmed_device(user):
                messages.error(request, NO_DEVICE_MESSAGE)
                return redirect(settings.LOGIN_URL)
            start_challenge(
                request, user, user.backend, oidc_id_token=token.get("id_token")
            )
            return redirect("identite:otp_verify")

        login(request, user, backend=user.backend)
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
        404: GenericErrorSerializer,
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
            return Response(
                GenericErrorSerializer({"error": "Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            self.logger.error("Unexpected error in UserInfoView: %s", str(e))
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
