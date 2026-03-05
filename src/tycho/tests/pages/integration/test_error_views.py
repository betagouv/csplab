from http import HTTPStatus

import pytest
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import Client, override_settings
from django.urls import include, path
from pytest_django.asserts import assertTemplateUsed


def _raise_403_view(request: object) -> HttpResponse:
    raise PermissionDenied


def _raise_500_view(request: object) -> HttpResponse:
    raise Exception("Simulated server error")


urlpatterns = [
    path("", include("presentation.pages.urls")),
    path("test-403/", _raise_403_view),
    path("test-500/", _raise_500_view),
]

_URL_CONF = "tests.pages.integration.test_error_views"


class TestErrorPages:
    @pytest.mark.parametrize(
        ("url", "expected_status", "expected_template"),
        [
            ("/test-403/", HTTPStatus.FORBIDDEN, "403.html"),
            ("/this-page-does-not-exist/", HTTPStatus.NOT_FOUND, "404.html"),
        ],
    )
    @override_settings(ROOT_URLCONF=_URL_CONF)
    def test_error_page(
        self,
        client: Client,
        db: None,
        url: str,
        expected_status: HTTPStatus,
        expected_template: str,
    ) -> None:
        response = client.get(url)
        assert response.status_code == expected_status
        assertTemplateUsed(response, expected_template)

    @override_settings(ROOT_URLCONF=_URL_CONF)
    def test_500_page(self, client: Client, db: None) -> None:
        client.raise_request_exception = False
        response = client.get("/test-500/")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assertTemplateUsed(response, "500.html")
