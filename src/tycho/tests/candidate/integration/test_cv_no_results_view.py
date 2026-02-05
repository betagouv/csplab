"""Integration tests for CV no results page view."""

from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed


def test_cv_no_results_view_renders(client, db):
    """GET returns 200 with template, heading, and placeholder message."""
    cv_uuid = uuid4()
    response = client.get(
        reverse("candidate:cv_no_results", kwargs={"cv_uuid": cv_uuid})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_no_results.html")
    assertContains(response, "Aucun résultat trouvé")
    assertContains(response, "fr-alert")  # DSFR alert component
