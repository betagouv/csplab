"""Integration tests for CV results page view."""

from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.utils.cv_test_utils import create_cv_in_database


def test_cv_results_page_loads_correctly(client, db):
    """GET returns 200 with template, title, breadcrumb, and all results."""
    cv_uuid = create_cv_in_database()
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
    cv_uuid = create_cv_in_database()
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
    cv_uuid = create_cv_in_database()
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
    cv_uuid = create_cv_in_database()
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        {"filter-location": "bordeaux"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "0 résultat")


@pytest.mark.parametrize(
    "status,is_htmx,expected_template,expected_content,unexpected_content",
    [
        (
            CVStatus.PENDING,
            False,
            "candidate/cv_processing.html",
            ["Analyse de votre CV en cours...", "hx-get", 'hx-trigger="load delay:2s"'],
            [],
        ),
        (
            CVStatus.PENDING,
            True,
            "candidate/components/_processing_content.html",
            ["Analyse de votre CV en cours...", 'hx-trigger="load delay:2s"'],
            ["<html", "<!DOCTYPE"],
        ),
        (
            CVStatus.COMPLETED,
            False,
            "candidate/cv_results.html",
            ["Vos opportunités professionnelles"],
            ['hx-trigger="load', 'hx-swap="outerHTML"'],
        ),
        (
            CVStatus.COMPLETED,
            True,
            "candidate/components/_results_content.html",
            ["Vos opportunités professionnelles"],
            ["<html", "<!DOCTYPE"],
        ),
    ],
)
@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_view_renders_correct_template_based_on_status(  # noqa: PLR0913
    mock_get_status,
    client,
    db,
    status,
    is_htmx,
    expected_template,
    expected_content,
    unexpected_content,
):
    """View renders appropriate template based on CV status and HTMX context."""
    cv_uuid = uuid4()
    mock_get_status.return_value = {"status": status, "opportunities": []}

    headers = {"HTTP_HX_REQUEST": "true"} if is_htmx else {}
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}), **headers
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, expected_template)
    for content in expected_content:
        assertContains(response, content)
    for content in unexpected_content:
        assertNotContains(response, content)


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_processing_flow_pending_to_completed(mock_get_status, client, db):
    """Full polling flow: initial PENDING request → HTMX poll → COMPLETED transition."""
    cv_uuid = uuid4()
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid})

    mock_get_status.return_value = {"status": CVStatus.PENDING}
    response_initial = client.get(url)
    assert response_initial.status_code == HTTPStatus.OK
    assertTemplateUsed(response_initial, "candidate/cv_processing.html")
    assertContains(response_initial, 'hx-trigger="load delay:2s"')

    response_poll = client.get(url, HTTP_HX_REQUEST="true")
    assert response_poll.status_code == HTTPStatus.OK
    assertTemplateUsed(response_poll, "candidate/components/_processing_content.html")
    assertContains(response_poll, 'hx-trigger="load delay:2s"')

    mock_get_status.return_value = {"status": CVStatus.COMPLETED, "opportunities": []}
    response_completed = client.get(url, HTTP_HX_REQUEST="true")
    assert response_completed.status_code == HTTPStatus.OK
    assertTemplateUsed(response_completed, "candidate/components/_results_content.html")
    assertContains(response_completed, "Vos opportunités professionnelles")
    assertNotContains(response_completed, 'hx-trigger="load')


def test_cv_results_with_pending_cv_in_database_shows_processing(client, db):
    """Real CV with PENDING status in DB shows processing template."""
    cv_metadata = CVMetadataFactory.build(status=CVStatus.PENDING)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_processing.html")
    assertContains(response, "Analyse de votre CV en cours...")
    assertContains(response, 'hx-trigger="load delay:2s"')


def test_cv_results_with_completed_cv_in_database_shows_results(client, db):
    """Real CV with COMPLETED status in DB shows results template."""
    cv_metadata = CVMetadataFactory.build(status=CVStatus.COMPLETED)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Vos opportunités professionnelles")


def test_cv_results_htmx_poll_pending_to_completed_transition(client, db):
    """HTMX polling detects status change from PENDING to COMPLETED in DB."""
    cv_metadata = CVMetadataFactory.build(status=CVStatus.PENDING)
    model = CVMetadataModel.from_entity(cv_metadata)
    model.save()
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})

    response_pending = client.get(url, HTTP_HX_REQUEST="true")
    assertTemplateUsed(
        response_pending, "candidate/components/_processing_content.html"
    )
    assertContains(response_pending, 'hx-trigger="load delay:2s"')

    model.status = CVStatus.COMPLETED.value
    model.save()

    response_completed = client.get(url, HTTP_HX_REQUEST="true")
    assertTemplateUsed(response_completed, "candidate/components/_results_content.html")
    assertContains(response_completed, "Vos opportunités professionnelles")
    assertNotContains(response_completed, 'hx-trigger="load')


def test_cv_results_nonexistent_cv_shows_pending(client, db):
    """CV not found in DB defaults to PENDING status (processing view)."""
    response = client.get(reverse("candidate:cv_results", kwargs={"cv_uuid": uuid4()}))

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_processing.html")
