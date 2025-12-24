"""Integration tests for home page view."""

from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):
    """Tests for the HomeView landing page."""

    def test_home_page_returns_200(self):
        """Homepage should return HTTP 200."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_contains_csplab_branding(self):
        """Homepage should contain CSPLab branding."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "CSPLab")

    def test_home_page_uses_correct_template(self):
        """Homepage should use home.html template."""
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "candidate/home.html")
