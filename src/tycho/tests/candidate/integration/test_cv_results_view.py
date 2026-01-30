"""Integration tests for CV results page view."""

from http import HTTPStatus
from uuid import uuid4

from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed


def test_cv_results_page_loads_correctly(client, db):
    """GET returns 200 with correct template, title, and breadcrumb."""
    cv_uuid = uuid4()
    response = client.get(reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}))
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Vos opportunités professionnelles")
    assertContains(response, "fr-breadcrumb")


def test_cv_results_invalid_uuid_returns_404(client, db):
    """Invalid UUID format in URL returns 404."""
    response = client.get("/candidate/cv/invalid-uuid/results/")
    assert response.status_code == HTTPStatus.NOT_FOUND
