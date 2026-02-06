"""Integration tests for CV results page view."""

from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.cv_metadata_factory import CVMetadataFactory


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_page_loads_correctly(
    mock_execute, client, db, concours, db_cv_uuid
):
    """GET returns 200 with template, title, breadcrumb, and all results."""
    # Mock the usecase to return mock results with proper format
    mock_execute.return_value = [(concours[0], 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid})
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Vos opportunités professionnelles")
    assertContains(response, "fr-breadcrumb")


def test_cv_results_invalid_uuid_returns_404(client, db):
    """Invalid UUID format in URL returns 404."""
    response = client.get("/candidate/cv/invalid-uuid/results/")
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_request_returns_partial(
    mock_execute, client, db, db_cv_uuid, concours
):
    """HTMX request returns partial template with results only."""
    # Mock the usecase to return mock results with proper format
    mock_execute.return_value = [(concours[0], 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_content.html")
    assertContains(response, "opportunités")


# TODO - add vectorized offers in test
@pytest.mark.parametrize(
    "filter_test_case",
    [
        {
            "filters": {"filter-location": "paris"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": ["Responsable des ressources humaines"],
        },
        {
            "filters": {"filter-location": "lyon"},
            "expected_titles": ["Responsable des ressources humaines"],
            "excluded_titles": ["Chef de projet transformation numérique"],
        },
        {
            "filters": {"filter-category": "b"},
            "expected_titles": ["Technicien informatique"],
            "excluded_titles": ["Chef de projet transformation numérique"],
        },
        {
            "filters": {"filter-location": "paris", "filter-category": "a"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": [
                "Technicien informatique",
                "Responsable des ressources humaines",
            ],
        },
        {
            "filters": {"filter-location": "bordeaux"},
            "expected_titles": [],
            "excluded_titles": ["Chef de projet transformation numérique"],
        },
        {
            "filters": {"filter-location": ""},
            "expected_titles": [
                "Chef de projet transformation numérique",
                "Responsable des ressources humaines",
                "Technicien informatique",
            ],
            "excluded_titles": [],
        },
        {
            "filters": {"filter-category": ""},
            "expected_titles": [
                "Chef de projet transformation numérique",
                "Responsable des ressources humaines",
                "Technicien informatique",
            ],
            "excluded_titles": [],
        },
    ],
)
@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_htmx_filter_returns_filtered_results(
    mock_get_status, client, db, filter_test_case, db_cv_uuid
):
    """HTMX filter request returns only matching results."""
    # Mock opportunities data that matches the filter expectations
    mock_opportunities = [
        {
            "title": "Chef de projet transformation numérique",
            "location_value": "paris",
            "category_value": "a",
            "type": "concours",
        },
        {
            "title": "Responsable des ressources humaines",
            "location_value": "lyon",
            "category_value": "a",
            "type": "concours",
        },
        {
            "title": "Technicien informatique",
            "location_value": "marseille",
            "category_value": "b",
            "type": "concours",
        },
    ]
    mock_get_status.return_value = {
        "status": CVStatus.COMPLETED,
        "opportunities": mock_opportunities,
    }

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        filter_test_case["filters"],
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    for title in filter_test_case["expected_titles"]:
        assertContains(response, title)
    for title in filter_test_case["excluded_titles"]:
        assertNotContains(response, title)


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_htmx_no_match_displays_empty_state(
    mock_get_status, client, db, db_cv_uuid
):
    """HTMX filter with no matches shows zero results message."""
    # Mock opportunities data that won't match the bordeaux filter
    mock_opportunities = [
        {
            "title": "Chef de projet transformation numérique",
            "location_value": "paris",
            "category_value": "a",
            "type": "concours",
        },
        {
            "title": "Responsable des ressources humaines",
            "location_value": "lyon",
            "category_value": "a",
            "type": "concours",
        },
    ]
    mock_get_status.return_value = {
        "status": CVStatus.COMPLETED,
        "opportunities": mock_opportunities,
    }

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        {"filter-location": "bordeaux"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    assertContains(response, "0 résultat")


@pytest.mark.parametrize(
    "test_case",
    [
        {
            "status": CVStatus.PENDING,
            "is_htmx": False,
            "expected_template": "candidate/cv_processing.html",
            "expected_content": [
                "Analyse de votre CV en cours...",
                "hx-get",
                'hx-trigger="every',
            ],
            "unexpected_content": [],
        },
        {
            "status": CVStatus.PENDING,
            "is_htmx": True,
            "expected_template": "candidate/components/_processing_content.html",
            "expected_content": [
                "Analyse de votre CV en cours...",
            ],
            "unexpected_content": ["<html", "<!DOCTYPE"],
            "expected_status": HTTPStatus.NO_CONTENT,
        },
        {
            "status": CVStatus.COMPLETED,
            "is_htmx": False,
            "expected_template": "candidate/cv_results.html",
            "expected_content": ["Vos opportunités professionnelles"],
            "unexpected_content": ['hx-trigger="load', 'hx-swap="outerHTML"'],
        },
        {
            "status": CVStatus.COMPLETED,
            "is_htmx": True,
            "expected_template": "candidate/components/_results_content.html",
            "expected_content": ["Vos opportunités professionnelles"],
            "unexpected_content": ["<html", "<!DOCTYPE"],
        },
    ],
)
@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_view_renders_correct_template_based_on_status(
    mock_get_status,
    client,
    db,
    db_cv_uuid,
    test_case,
):
    """View renders appropriate template based on CV status and HTMX context."""
    opportunities = (
        [{"title": "Test opportunity"}]
        if test_case["status"] == CVStatus.COMPLETED
        else []
    )
    mock_get_status.return_value = {
        "status": test_case["status"],
        "opportunities": opportunities,
    }

    headers = {"HTTP_HX_REQUEST": "true"} if test_case["is_htmx"] else {}
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}), **headers
    )

    expected_status = test_case.get("expected_status", HTTPStatus.OK)
    assert response.status_code == expected_status

    if expected_status == HTTPStatus.OK:
        assertTemplateUsed(response, test_case["expected_template"])
        for content in test_case["expected_content"]:
            assertContains(response, content)
        for content in test_case["unexpected_content"]:
            assertNotContains(response, content)
    elif expected_status == HTTPStatus.NO_CONTENT:
        # For 204 responses, check headers instead of content
        assert "HX-Reswap" in response
        assert response["HX-Reswap"] == "none"


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_processing_flow_pending_to_completed(
    mock_get_status, client, db, db_cv_uuid
):
    """Full polling flow: initial PENDING request → HTMX poll → COMPLETED transition."""
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid})

    mock_get_status.return_value = {"status": CVStatus.PENDING}
    response_initial = client.get(url)
    assert response_initial.status_code == HTTPStatus.OK
    assertTemplateUsed(response_initial, "candidate/cv_processing.html")
    assertContains(
        response_initial,
        f'hx-trigger="every {settings.CV_PROCESSING_POLL_INTERVAL}s"',
    )

    response_poll = client.get(url, HTTP_HX_REQUEST="true")
    assert response_poll.status_code == HTTPStatus.NO_CONTENT
    assert response_poll["HX-Reswap"] == "none"

    mock_get_status.return_value = {
        "status": CVStatus.COMPLETED,
        "opportunities": [{"title": "Test opportunity"}],
    }
    response_completed = client.get(url, HTTP_HX_REQUEST="true")
    assert response_completed.status_code == HTTPStatus.OK
    assertTemplateUsed(response_completed, "candidate/components/_results_content.html")
    assertContains(response_completed, "Vos opportunités professionnelles")
    assertNotContains(response_completed, 'hx-trigger="every')


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
    assertContains(
        response, f'hx-trigger="every {settings.CV_PROCESSING_POLL_INTERVAL}s"'
    )


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_with_completed_cv_in_database_shows_results(
    mock_execute, client, db, concours
):
    """Real CV with COMPLETED status in DB shows results template."""
    mock_execute.return_value = [(concours[0], 0.9)]
    cv_metadata = CVMetadataFactory.build(status=CVStatus.COMPLETED)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Vos opportunités professionnelles")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_poll_pending_to_completed_transition(
    mock_execute, client, db, concours
):
    """HTMX polling detects status change from PENDING to COMPLETED in DB."""
    mock_execute.return_value = [(concours[0], 0.9)]
    cv_metadata = CVMetadataFactory.build(status=CVStatus.PENDING)
    model = CVMetadataModel.from_entity(cv_metadata)
    model.save()
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})

    response_pending = client.get(url, HTTP_HX_REQUEST="true")
    assert response_pending.status_code == HTTPStatus.NO_CONTENT
    assert response_pending["HX-Reswap"] == "none"

    model.status = CVStatus.COMPLETED.value
    model.save()

    response_completed = client.get(url, HTTP_HX_REQUEST="true")
    assertTemplateUsed(response_completed, "candidate/components/_results_content.html")
    assertContains(response_completed, "Vos opportunités professionnelles")
    assertNotContains(response_completed, 'hx-trigger="every')


def test_cv_results_nonexistent_cv_redirects_to_upload(client, db):
    """CV not found in DB redirects to upload view due to container creation failure."""
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": uuid4()}), follow=True
    )

    assert response.status_code == HTTPStatus.OK
    assert response.redirect_chain[0] == (
        reverse("candidate:cv_upload"),
        HTTPStatus.FOUND,
    )
    assertContains(
        response,
        "Une erreur est survenue lors du traitement de votre CV. Veuillez réessayer.",
    )


def test_cv_results_failed_status_redirects_with_error_message(client, db):
    """CV with FAILED status redirects to cv-upload with French error message."""
    cv_metadata = CVMetadataFactory.build(status=CVStatus.FAILED)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        follow=True,
    )

    assertRedirects(
        response,
        reverse("candidate:cv_upload"),
        target_status_code=HTTPStatus.OK,
    )
    assertContains(
        response,
        "Une erreur est survenue lors du traitement de votre CV. Veuillez réessayer.",
    )


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_htmx_request_sets_redirect_header(mock_get_status, client, db):
    """HTMX request with FAILED status sets HX-Redirect header."""
    cv_uuid = uuid4()
    mock_get_status.return_value = {"status": CVStatus.FAILED, "opportunities": []}

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assert "HX-Redirect" in response
    assert response["HX-Redirect"] == reverse("candidate:cv_upload")


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_shows_no_results_when_empty(mock_get_status, client, db):
    """CV with COMPLETED status and empty opportunities shows no-results template."""
    cv_uuid = uuid4()
    mock_get_status.return_value = {"status": CVStatus.COMPLETED, "opportunities": []}

    response = client.get(reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}))

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "0 résultats")
    assertContains(response, "Aucun résultat pour le moment")


@patch("presentation.candidate.views.cv_flow.CVResultsView._get_cv_processing_status")
def test_cv_results_htmx_empty_opportunities_shows_no_results(
    mock_get_status, client, db
):
    """HTMX request with empty opportunities shows no-results template."""
    cv_uuid = uuid4()
    mock_get_status.return_value = {"status": CVStatus.COMPLETED, "opportunities": []}

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_uuid}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_no_results_content.html")
    assertContains(response, "Aucun résultat trouvé")
