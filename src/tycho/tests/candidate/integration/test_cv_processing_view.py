"""Integration tests for CV processing page view."""

from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed


class TestCVProcessingView:
    """Tests for the CVProcessingView page."""

    def test_cv_processing_page(self, client, db):
        """Test CV processing page response and template."""
        cv_uuid = uuid4()
        response = client.get(
            reverse("candidate:cv_processing", kwargs={"cv_uuid": cv_uuid})
        )
        assert response.status_code == HTTPStatus.OK

        """CV processing page should use cv_processing.html template."""
        assertTemplateUsed(response, "candidate/cv_processing.html")

        """CV processing page should contain processing title."""
        assertContains(response, "Analyse de votre CV en cours...")
