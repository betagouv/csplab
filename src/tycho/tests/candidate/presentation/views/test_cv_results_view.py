from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertTemplateUsed,
)

from domain.entities.concours import Concours
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory


@pytest.fixture(name="concours")
def concours_fixture():
    return [
        Concours(
            nor_original=NOR("MENA2400001A"),
            nor_list=[NOR("MENA2400001A")],
            category=Category.A,
            ministry=Ministry.MAA,
            access_modality=[AccessModality.CONCOURS_EXTERNE],
            corps="Ingénieur des systèmes d'information",
            grade="Ingénieur principal",
            written_exam_date=datetime.now(timezone.utc),
            open_position_number=10,
        ),
        Concours(
            nor_original=NOR("AGRI2400002B"),
            nor_list=[NOR("AGRI2400002B")],
            category=Category.A,
            ministry=Ministry.MAA,
            access_modality=[AccessModality.CONCOURS_EXTERNE],
            corps="Attaché d'administration",
            grade="Attaché principal",
            written_exam_date=datetime.now(timezone.utc),
            open_position_number=5,
        ),
    ]


@pytest.fixture(name="db_cv_uuid")
def db_cv_uuid_fixture(status: CVStatus = CVStatus.COMPLETED) -> UUID:
    cv_metadata = CVMetadataFactory.build(
        status=status, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    return cv_metadata.id


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_page_loads_correctly(
    mock_execute, client, db, concours, db_cv_uuid
):
    # Mock the usecase to return mock results with proper format
    mock_execute.return_value = [(concours[0], 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid})
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Offres et concours les plus pertinents")
    assertContains(response, "fr-breadcrumb")


def test_cv_results_invalid_uuid_returns_404(client, db):
    response = client.get("/candidate/cv/invalid-uuid/results/")
    assert response.status_code == HTTPStatus.NOT_FOUND


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_request_returns_partial(
    mock_execute, client, db, db_cv_uuid, concours
):
    # Mock the usecase to return mock results with proper format
    mock_execute.return_value = [(concours[0], 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_content.html")
    assertContains(response, "Offres et concours")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_no_match_displays_empty_state(
    mock_execute, client, db, db_cv_uuid
):
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        {"filter-location": "33"},
        HTTP_HX_REQUEST="true",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_no_results_content.html")
    assertContains(response, "nous n'avons pas trouvé d'opportunité")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_results_zone_target_returns_results_list_template(
    mock_execute, client, db
):
    cv_metadata = CVMetadataFactory.build(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    mock_execute.return_value = [(OfferFactory.build(title="Poste ciblé"), 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        HTTP_HX_REQUEST="true",
        HTTP_HX_TARGET="results-zone",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    assertContains(response, "Poste ciblé")


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
            "expected_status": HTTPStatus.NO_CONTENT,
        },
        {
            "status": CVStatus.COMPLETED,
            "is_htmx": False,
            "expected_template": "candidate/cv_results.html",
            "expected_content": ["Offres et concours les plus pertinents"],
            "unexpected_content": ['hx-trigger="load', 'hx-swap="outerHTML"'],
        },
        {
            "status": CVStatus.COMPLETED,
            "is_htmx": True,
            "expected_template": "candidate/components/_results_content.html",
            "expected_content": ["Offres et concours les plus pertinents"],
            "unexpected_content": ["<html", "<!DOCTYPE"],
        },
    ],
)
@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_view_renders_correct_template_based_on_status(
    mock_execute,
    client,
    db,
    test_case,
):
    cv_metadata = CVMetadataFactory.build(
        status=test_case["status"], search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    mock_execute.return_value = (
        [(OfferFactory.build(title="Test opportunity"), 0.9)]
        if test_case["status"] == CVStatus.COMPLETED
        else []
    )

    headers = {"HTTP_HX_REQUEST": "true"} if test_case["is_htmx"] else {}
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}), **headers
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


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_poll_pending_to_completed_transition(
    mock_execute, client, db, concours
):
    mock_execute.return_value = [(concours[0], 0.9)]
    cv_metadata = CVMetadataFactory.build(status=CVStatus.PENDING)
    model = CVMetadataModel.from_entity(cv_metadata)
    model.save()
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})

    response_pending = client.get(url, {"poll": "1"}, HTTP_HX_REQUEST="true")
    assert response_pending.status_code == HTTPStatus.NO_CONTENT
    assert response_pending["HX-Reswap"] == "none"

    model.status = CVStatus.COMPLETED.value
    model.save()

    response_completed = client.get(url, {"poll": "1"}, HTTP_HX_REQUEST="true")
    assert response_completed.status_code == HTTPStatus.OK
    assert response_completed["HX-Redirect"] == url


def test_cv_results_nonexistent_cv_redirects_to_upload(client, db):
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


def test_cv_results_htmx_request_sets_redirect_header(client, db):
    cv_metadata = CVMetadataFactory.build(status=CVStatus.FAILED)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assert "HX-Redirect" in response
    assert response["HX-Redirect"] == reverse("candidate:cv_upload")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_empty_opportunities_shows_no_results(mock_execute, client, db):
    cv_metadata = CVMetadataFactory.build(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_no_results_content.html")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_no_results_includes_tally_iframe(
    mock_execute, client, db, settings
):
    cv_metadata = CVMetadataFactory.build(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    settings.TALLY_FORM_ID_NO_RESULTS = "test-no-results-form"
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-no-results-form")
    assertContains(response, f"cv_uuid={cv_metadata.id}")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_with_results_includes_tally_modal(
    mock_execute, client, db, settings
):
    cv_metadata = CVMetadataFactory.build(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    settings.TALLY_FORM_ID_RESULTS = "test-results-form"
    mock_execute.return_value = [(OfferFactory.build(title="Poste test"), 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-results-form")
    assertContains(response, f"cv_uuid={cv_metadata.id}")
    assertContains(response, "tally-results-modal")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_pagination_with_filters(mock_execute, client, db, settings):
    cv_metadata = CVMetadataFactory.build(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    settings.CV_RESULTS_PER_PAGE = 1
    mock_execute.return_value = [
        (OfferFactory.build(title=f"Paris {i}", department="75"), 0.9 - i * 0.01)
        for i in range(3)
    ]
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}),
        {"filter-location": "75", "page": "2"},
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Paris 1")
    assertNotContains(response, "Paris 0")
