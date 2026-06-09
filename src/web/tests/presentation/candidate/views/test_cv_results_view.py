from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertTemplateUsed

from domain.candidate.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.candidate.cv_metadata_factory import CVMetadataFactory
from tests.factories.referentiel.offer_factory import OfferFactory


@pytest.fixture
def cv_metadata_completed():
    return CVMetadataFactory.create_entity(
        status=CVStatus.COMPLETED, search_query="Python developer"
    )


@pytest.fixture
def cv_metadata_pending():
    return CVMetadataFactory.create_entity(
        status=CVStatus.PENDING, search_query="Python developer"
    )


@pytest.fixture
def mock_execute():
    with patch(
        "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
    ) as mock:
        yield mock


def test_cv_results_invalid_uuid_returns_404(client, db):
    response = client.get("/candidate/cv/invalid-uuid/results/")

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    ("status", "is_htmx", "expected_status", "expected_template"),
    [
        (CVStatus.PENDING, False, HTTPStatus.OK, "candidate/cv_processing.html"),
        (CVStatus.PENDING, True, HTTPStatus.NO_CONTENT, None),
        (CVStatus.COMPLETED, False, HTTPStatus.OK, "candidate/cv_results.html"),
        (
            CVStatus.COMPLETED,
            True,
            HTTPStatus.OK,
            "candidate/components/_results_content.html",
        ),
    ],
)
def test_cv_results_selects_response_from_status_and_request_type(
    mock_execute,
    client,
    db,
    status,
    is_htmx,
    expected_status,
    expected_template,
):
    cv_metadata = CVMetadataFactory.create_entity(
        status=status,
        search_query="Python developer",
    )
    CVMetadataModel.from_entity(cv_metadata).save()
    mock_execute.return_value = [
        ((OfferFactory.create_entity(title="Poste test"), []), 0.9)
    ]

    headers = {"HTTP_HX_REQUEST": "true"} if is_htmx else {}
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}),
        **headers,
    )

    assert response.status_code == expected_status

    if expected_status == HTTPStatus.NO_CONTENT:
        assert response["HX-Reswap"] == "none"
        mock_execute.assert_not_called()
        return

    assertTemplateUsed(response, expected_template)

    if status == CVStatus.COMPLETED:
        mock_execute.assert_called_once()
    else:
        mock_execute.assert_not_called()


def test_cv_results_htmx_results_zone_target_returns_results_list_template(
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = [
        ((OfferFactory.create_entity(title="Poste ciblé"), []), 0.9)
    ]

    response = client.get(
        reverse(
            "candidate:cv_results",
            kwargs={"cv_uuid": cv_metadata_completed.entity_id},
        ),
        HTTP_HX_REQUEST="true",
        HTTP_HX_TARGET="results-zone",
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    assertContains(response, "Poste ciblé")


def test_cv_results_htmx_poll_pending_to_completed_transition(
    mock_execute, client, db, cv_metadata_pending
):
    model = CVMetadataModel.from_entity(cv_metadata_pending)
    model.save()
    mock_execute.return_value = [
        ((OfferFactory.create_entity(title="Poste test"), []), 0.9)
    ]
    url = reverse(
        "candidate:cv_results", kwargs={"cv_uuid": cv_metadata_pending.entity_id}
    )

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
        reverse("candidate:cv_results", kwargs={"cv_uuid": uuid4()}),
        follow=True,
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
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.FAILED)
    CVMetadataModel.from_entity(cv_metadata).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assert response["HX-Redirect"] == reverse("candidate:cv_upload")


def test_cv_results_htmx_empty_opportunities_shows_no_results(
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = []

    response = client.get(
        reverse(
            "candidate:cv_results",
            kwargs={"cv_uuid": cv_metadata_completed.entity_id},
        ),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_no_results_content.html")


def test_cv_results_no_results_includes_tally_iframe(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.TALLY_FORM_ID_NO_RESULTS = "test-no-results-form"
    mock_execute.return_value = []

    response = client.get(
        reverse(
            "candidate:cv_results",
            kwargs={"cv_uuid": cv_metadata_completed.entity_id},
        ),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-no-results-form")
    assertContains(response, f"cv_uuid={cv_metadata_completed.entity_id}")


def test_cv_results_with_results_includes_tally_modal(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.TALLY_FORM_ID_RESULTS = "test-results-form"
    mock_execute.return_value = [
        ((OfferFactory.create_entity(title="Poste test"), []), 0.9)
    ]

    response = client.get(
        reverse(
            "candidate:cv_results",
            kwargs={"cv_uuid": cv_metadata_completed.entity_id},
        )
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-results-form")
    assertContains(response, f"cv_uuid={cv_metadata_completed.entity_id}")
    assertContains(response, "tally-results-modal")
