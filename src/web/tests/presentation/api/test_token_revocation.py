from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from application.identite.services.deactivate_api_account import (
    deactivate_api_account,
)
from application.identite.services.revoke_api_tokens import revoke_api_tokens
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD

JWT_ROUTE = reverse("ingestion:offers_list")


def _obtain(api_client, user):
    response = api_client.post(
        reverse("api:token_obtain_pair"),
        {"email": user.email, "password": DEFAULT_PASSWORD},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()["refresh"]


def _refresh(api_client, refresh):
    return api_client.post(
        reverse("api:token_refresh"), {"refresh": refresh}, format="json"
    )


def test_obtaining_a_token_tracks_the_refresh_token_without_storing_it(
    api_client, test_user
):
    refresh = RefreshToken(_obtain(api_client, test_user))

    outstanding = OutstandingToken.objects.get()
    assert outstanding.user == test_user
    assert outstanding.jti == refresh["jti"]
    assert outstanding.token == ""


def test_a_revoked_refresh_token_is_rejected(api_client, test_user):
    refresh = _obtain(api_client, test_user)

    revoke_api_tokens(compte=test_user, utilisateur=UtilisateurDjangoFactory())

    response = _refresh(api_client, refresh)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["code"] == "token_not_valid"


def test_a_token_obtained_after_the_revocation_works(api_client, test_user):
    revoke_api_tokens(compte=test_user, utilisateur=UtilisateurDjangoFactory())

    response = _refresh(api_client, _obtain(api_client, test_user))

    assert response.status_code == status.HTTP_200_OK


class TestDeactivatedAccount:
    def test_cannot_obtain_a_token(self, api_client, test_user):
        deactivate_api_account(compte=test_user, utilisateur=UtilisateurDjangoFactory())

        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": DEFAULT_PASSWORD},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_refresh_nor_use_a_token_obtained_before(
        self, api_client, test_user
    ):
        response = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": test_user.email, "password": DEFAULT_PASSWORD},
            format="json",
        )
        tokens = response.json()

        deactivate_api_account(compte=test_user, utilisateur=UtilisateurDjangoFactory())

        assert (
            _refresh(api_client, tokens["refresh"]).status_code
            == status.HTTP_401_UNAUTHORIZED
        )
        call = api_client.get(
            JWT_ROUTE, HTTP_AUTHORIZATION=f"Bearer {tokens['access']}"
        )
        assert call.status_code == status.HTTP_401_UNAUTHORIZED
