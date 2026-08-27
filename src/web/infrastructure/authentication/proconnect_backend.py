from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse

from application.identite.usecases.log_utilisateur_connexion import (
    LogUtilisateurConnexionInput,
)
from infrastructure.authentication.proconnect_client import END_SESSION_ENDPOINT
from infrastructure.di.identite.identite_factory import create_identite_container
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper


def build_proconnect_logout_url(request, id_token: str) -> str:
    post_logout_redirect_uri = request.build_absolute_uri(reverse("pages:home"))
    params = {
        "id_token_hint": id_token,
        "post_logout_redirect_uri": post_logout_redirect_uri,
    }
    logout_url = f"{settings.PROCONNECT_BASE_URL}{END_SESSION_ENDPOINT}"
    return f"{logout_url}?{urlencode(params)}"


class ProconnectBackend(ModelBackend):
    def __init__(self):
        self.container = create_identite_container()
        self.logger = self.container.logger_service()
        self._mapper = UtilisateurMapper()

    def authenticate(self, request, proconnect_claims=None, **kwargs):
        if not proconnect_claims or not proconnect_claims.get("email"):
            return None
        user = (
            get_user_model()
            .objects.filter(email__iexact=proconnect_claims["email"], is_active=True)
            .first()
        )
        if user is not None:
            self._audit_connexion(user)
        return user

    def _audit_connexion(self, user) -> None:
        # Auditing must never break the login flow, mirrors
        # presentation.identite.views.LoginView._audit_connexion.
        try:
            usecase = self.container.log_utilisateur_connexion_usecase()
            usecase.execute(
                LogUtilisateurConnexionInput(utilisateur=self._mapper.to_domain(user))
            )
        except Exception as e:
            self.logger.error("Failed to audit ProConnect login: %s", str(e))
