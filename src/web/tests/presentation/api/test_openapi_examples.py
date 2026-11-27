import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.django_apps.users.models import AllowedNetworkModel
from presentation.api import openapi_examples
from tests.utils.openapi_test_utils import assert_matches_openapi_schema

API_KEY = "secret-key"
ALLOWED_IP = "203.0.113.7"
OTHER_IP = "198.51.100.1"
JWT_ROUTE = reverse("ingestion:offers_list")
API_KEY_ROUTE = reverse("ingestion:organismes_upsert")


def _jwt(user):
    return f"Bearer {RefreshToken.for_user(user).access_token}"


def _invalid_jwt(api_client, user):
    return api_client.get(JWT_ROUTE, HTTP_AUTHORIZATION="Bearer invalid")


def _jwt_ip_not_allowed(api_client, user):
    AllowedNetworkModel.objects.create(user=user, cidr="203.0.113.0/24", label="NAT")
    return api_client.get(
        JWT_ROUTE, HTTP_AUTHORIZATION=_jwt(user), HTTP_X_REAL_IP=OTHER_IP
    )


def _invalid_api_key(api_client, user):
    return api_client.get(JWT_ROUTE, HTTP_AUTHORIZATION="Api-Key wrong-key")


def _api_key_ip_not_allowed(api_client, user):
    return api_client.get(
        JWT_ROUTE, HTTP_AUTHORIZATION=f"Api-Key {API_KEY}", HTTP_X_REAL_IP=OTHER_IP
    )


def _jwt_on_api_key_route(api_client, user):
    return api_client.post(
        API_KEY_ROUTE, {}, format="json", HTTP_AUTHORIZATION=_jwt(user)
    )


@pytest.mark.parametrize(
    "example, call",
    [
        (openapi_examples.INVALID_JWT, _invalid_jwt),
        (openapi_examples.JWT_IP_NOT_ALLOWED, _jwt_ip_not_allowed),
        (openapi_examples.INVALID_API_KEY, _invalid_api_key),
        (openapi_examples.API_KEY_IP_NOT_ALLOWED, _api_key_ip_not_allowed),
        (openapi_examples.JWT_ON_API_KEY_ROUTE, _jwt_on_api_key_route),
    ],
    ids=lambda value: getattr(value, "name", None),
)
def test_example_matches_the_returned_body(
    api_client, test_user, settings, example, call
):
    settings.INGESTION_API_KEY = API_KEY
    settings.INGESTION_API_KEY_ALLOWED_IP_RANGES = [f"{ALLOWED_IP}/32"]

    response = call(api_client, test_user)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == example.value
    assert_matches_openapi_schema(
        response.json(),
        response.request["PATH_INFO"],
        method=response.request["REQUEST_METHOD"],
        status_code="401",
    )
