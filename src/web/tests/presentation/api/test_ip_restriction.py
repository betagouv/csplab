import logging
from unittest.mock import patch

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.authentication.rejection import AuthRejectionRateThrottle
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.django_apps.users.models import AllowedNetworkModel
from infrastructure.factories.identite.utilisateur_factory import DEFAULT_PASSWORD

ALLOWED_IP = "203.0.113.7"
OTHER_IP = "198.51.100.1"
JWT_ROUTE = reverse("ingestion:offers_list")


@pytest.fixture(name="logs")
def logs_fixture(caplog):
    caplog.set_level(logging.INFO, logger="identite")
    return caplog


@pytest.fixture(name="restricted_user")
def restricted_user_fixture(test_user):
    AllowedNetworkModel.objects.create(
        user=test_user, cidr="203.0.113.0/24", label="NAT prod"
    )
    return test_user


def _obtain(api_client, user, ip):
    return api_client.post(
        reverse("api:token_obtain_pair"),
        {"email": user.email, "password": DEFAULT_PASSWORD},
        format="json",
        HTTP_X_REAL_IP=ip,
    )


def _refresh(api_client, user, ip):
    return api_client.post(
        reverse("api:token_refresh"),
        {"refresh": str(RefreshToken.for_user(user))},
        format="json",
        HTTP_X_REAL_IP=ip,
    )


def _call_jwt_route(api_client, user, ip):
    access = RefreshToken.for_user(user).access_token
    return api_client.get(
        JWT_ROUTE, HTTP_AUTHORIZATION=f"Bearer {access}", HTTP_X_REAL_IP=ip
    )


def _assert_rejection_audited(user, ip):
    attempt = AuditLoginLogModel.objects.get(resultat=Resultat.ECHEC)
    assert attempt.canal == Canal.JWT
    assert attempt.utilisateur_id == user.username
    assert attempt.ip_address == ip


class TestUnrestrictedAccount:
    @pytest.mark.parametrize("call", [_obtain, _refresh, _call_jwt_route])
    def test_is_accepted_from_any_ip(self, api_client, test_user, call):
        response = call(api_client, test_user, OTHER_IP)

        assert response.status_code == status.HTTP_200_OK


class TestRestrictedAccount:
    @pytest.mark.parametrize("call", [_obtain, _refresh, _call_jwt_route])
    def test_is_accepted_from_an_allowed_ip(self, api_client, restricted_user, call):
        response = call(api_client, restricted_user, ALLOWED_IP)

        assert response.status_code == status.HTTP_200_OK

    def test_obtain_is_refused_like_a_wrong_password(
        self, api_client, restricted_user, logs
    ):
        response = _obtain(api_client, restricted_user, OTHER_IP)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        expected_log = (
            f"JWT for user {restricted_user.pk} rejected (IP not allowed) "
            f"from {OTHER_IP}."
        )
        assert expected_log in [r.getMessage() for r in logs.records]
        _assert_rejection_audited(restricted_user, OTHER_IP)
        assert not AuditLoginLogModel.objects.filter(resultat=Resultat.SUCCES).exists()
        wrong_password = api_client.post(
            reverse("api:token_obtain_pair"),
            {"email": restricted_user.email, "password": "wrong"},
            format="json",
            HTTP_X_REAL_IP=ALLOWED_IP,
        )
        assert response.json() == wrong_password.json()

    @pytest.mark.parametrize("call", [_refresh, _call_jwt_route])
    def test_refresh_and_use_are_refused(self, api_client, restricted_user, call):
        response = call(api_client, restricted_user, OTHER_IP)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Authentication failed."
        _assert_rejection_audited(restricted_user, OTHER_IP)

    def test_unknown_client_ip_is_refused(self, api_client, restricted_user):
        access = RefreshToken.for_user(restricted_user).access_token

        response = api_client.get(JWT_ROUTE, HTTP_AUTHORIZATION=f"Bearer {access}")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_obtained_from_an_allowed_ip_is_refused_elsewhere(
        self, api_client, restricted_user
    ):
        access = _obtain(api_client, restricted_user, ALLOWED_IP).json()["access"]

        response = api_client.get(
            JWT_ROUTE, HTTP_AUTHORIZATION=f"Bearer {access}", HTTP_X_REAL_IP=OTHER_IP
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@patch.object(
    AuthRejectionRateThrottle, "THROTTLE_RATES", {"auth_rejection": "1/minute"}
)
def test_repeated_rejections_are_throttled_without_audit(api_client, restricted_user):
    cache.clear()
    assert (
        _call_jwt_route(api_client, restricted_user, OTHER_IP).status_code
        == status.HTTP_401_UNAUTHORIZED
    )

    response = _call_jwt_route(api_client, restricted_user, OTHER_IP)

    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert AuditLoginLogModel.objects.count() == 1
