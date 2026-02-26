"""Integration tests for custom error page views."""

from http import HTTPStatus

import pytest
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import Client, override_settings
from django.urls import include, path
from pytest_django.asserts import assertTemplateUsed

from config import urls as config_urls
from presentation.pages.views import custom_403_view, custom_404_view, custom_500_view


def _raise_403_view(request: object) -> HttpResponse:
    raise PermissionDenied


def _raise_500_view(request: object) -> HttpResponse:
    raise Exception("Simulated server error")


urlpatterns = [
    path("", include("presentation.pages.urls")),
    path("test-403/", _raise_403_view),
    path("test-500/", _raise_500_view),
]
handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

_URL_CONF = "tests.pages.integration.test_error_views"


class TestErrorViews:
    """Tests for custom error handler views."""

    @pytest.mark.parametrize(
        ("url", "expected_status", "expected_template"),
        [
            ("/test-403/", HTTPStatus.FORBIDDEN, "403.html"),
            ("/this-page-does-not-exist/", HTTPStatus.NOT_FOUND, "404.html"),
        ],
    )
    @override_settings(ROOT_URLCONF=_URL_CONF)
    def test_error_view(
        self,
        client: Client,
        db: None,
        url: str,
        expected_status: HTTPStatus,
        expected_template: str,
    ) -> None:
        """Error handler returns correct status and template."""
        response = client.get(url)
        assert response.status_code == expected_status
        assertTemplateUsed(response, expected_template)

    @override_settings(ROOT_URLCONF=_URL_CONF)
    def test_500_view(self, client: Client, db: None) -> None:
        """500 handler returns server error status with correct template."""
        client.raise_request_exception = False
        response = client.get("/test-500/")
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assertTemplateUsed(response, "500.html")


class TestErrorHandlersWiring:
    """Tests that the real URL conf has error handlers correctly wired."""

    def test_handlers_are_registered(self, db: None) -> None:
        """Verify config.urls declares all custom error handlers."""
        assert hasattr(config_urls, "handler403")
        assert hasattr(config_urls, "handler404")
        assert hasattr(config_urls, "handler500")
        assert config_urls.handler403 is custom_403_view
        assert config_urls.handler404 is custom_404_view
        assert config_urls.handler500 is custom_500_view
