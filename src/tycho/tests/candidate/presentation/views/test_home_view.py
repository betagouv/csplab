"""Integration tests for home page view."""

from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed


class TestHomeView:
    """Tests for the HomeView landing page."""

    def test_home_page(self, client, db):
        """Test home page response, branding and template."""
        response = client.get(reverse("pages:home"))
        assert response.status_code == HTTPStatus.OK

        """Homepage should contain CSPLab branding."""
        assertContains(response, "CSPLab")

        """Homepage should use home.html template."""
        assertTemplateUsed(response, "pages/home.html")
