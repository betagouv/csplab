"""Integration tests for CV results page view."""

from http import HTTPStatus
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed


def test_cv_results_page_loads_correctly(client, db):
    """GET returns 200 with template, title, breadcrumb, and all results."""
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


def test_cv_results_htmx_request_returns_partial(client, db):
    """HTMX request returns partial template with results only."""
    cv_uuid = uuid4()
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    assertContains(response, "résultat")


@pytest.mark.parametrize(
    "filters,expected_titles,excluded_titles",
    [
        (
            {"filter-location": "paris"},
            ["Chef de projet transformation numérique"],
            ["Responsable des ressources humaines"],
        ),
        (
            {"filter-location": "lyon"},
            ["Responsable des ressources humaines"],
            ["Chef de projet transformation numérique"],
        ),
        (
            {"filter-category": "b"},
            ["Technicien informatique"],
            ["Chef de projet transformation numérique"],
        ),
        (
            {"filter-location": "paris", "filter-category": "a"},
            ["Chef de projet transformation numérique"],
            ["Technicien informatique", "Responsable des ressources humaines"],
        ),
        (
            {"filter-location": "bordeaux"},
            [],
            ["Chef de projet transformation numérique"],
        ),
        (
            {"filter-location": ""},
            [
                "Chef de projet transformation numérique",
                "Responsable des ressources humaines",
                "Technicien informatique",
            ],
            [],
        ),
        (
            {"filter-category": ""},
            [
                "Chef de projet transformation numérique",
                "Responsable des ressources humaines",
                "Technicien informatique",
            ],
            [],
        ),
    ],
)
def test_cv_results_htmx_filter_returns_filtered_results(
    client, db, filters, expected_titles, excluded_titles
):
    """HTMX filter request returns only matching results."""
    cv_uuid = uuid4()
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        filters,
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    for title in expected_titles:
        assertContains(response, title)
    for title in excluded_titles:
        assertNotContains(response, title)


def test_cv_results_htmx_no_match_displays_empty_state(client, db):
    """HTMX filter with no matches shows zero results message."""
    cv_uuid = uuid4()
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        {"filter-location": "bordeaux"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "0 résultat")
