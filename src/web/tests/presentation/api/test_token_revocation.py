from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from application.identite.services.revoke_api_tokens import revoke_api_tokens
from infrastructure.django_apps.users.models import AllowedNetworkModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


def _obtain(api_client, user):
    return api_client.post(
        reverse("api:token_obtain_pair"),
        {"email": user.email, "password": DEFAULT_PASSWORD},
        format="json",
    )


def _refresh(api_client, refresh):
    return api_client.post(
        reverse("api:token_refresh"), {"refresh": refresh}, format="json"
    )


def test_obtaining_a_token_tracks_the_refresh_token_without_storing_it(
    api_client, test_user
):
    refresh = RefreshToken(_obtain(api_client, test_user).json()["refresh"])

    outstanding = OutstandingToken.objects.get()
    assert (outstanding.user, outstanding.jti, outstanding.token) == (
        test_user,
        refresh["jti"],
        "",
    )


def test_a_refresh_token_refused_for_its_ip_is_not_tracked(api_client, test_user):
    AllowedNetworkModel.objects.create(
        user=test_user, cidr="203.0.113.0/24", label="NAT prod"
    )

    response = api_client.post(
        reverse("api:token_obtain_pair"),
        {"email": test_user.email, "password": DEFAULT_PASSWORD},
        format="json",
        HTTP_X_REAL_IP="198.51.100.1",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not OutstandingToken.objects.exists()


def test_a_revoked_refresh_token_is_rejected(api_client, test_user):
    refresh = _obtain(api_client, test_user).json()["refresh"]

    revoke_api_tokens(account=test_user, actor=UtilisateurDjangoFactory())

    response = _refresh(api_client, refresh)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["code"] == "token_not_valid"


def test_a_deactivated_account_is_cut_off(api_client, test_user):
    tokens = _obtain(api_client, test_user).json()

    revoke_api_tokens(
        account=test_user, actor=UtilisateurDjangoFactory(), deactivate=True
    )

    call = api_client.get(
        reverse("ingestion:offers_list"),
        HTTP_AUTHORIZATION=f"Bearer {tokens['access']}",
    )
    assert call.status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        _refresh(api_client, tokens["refresh"]).status_code
        == status.HTTP_401_UNAUTHORIZED
    )
    assert _obtain(api_client, test_user).status_code == status.HTTP_401_UNAUTHORIZED
