from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from application.identite.services.revoke_api_tokens import revoke_api_tokens
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD


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


def test_obtaining_a_token_tracks_the_refresh_token(api_client, test_user):
    _obtain(api_client, test_user)

    assert OutstandingToken.objects.get().user == test_user


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
