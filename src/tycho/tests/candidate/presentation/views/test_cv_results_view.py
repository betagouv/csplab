from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
from django.conf import settings
from django.urls import reverse
from pytest_django.asserts import (
    assertContains,
    assertNotContains,
    assertRedirects,
    assertTemplateUsed,
)

from domain.entities.concours import Concours
from domain.value_objects.access_modality import AccessModality
from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from domain.value_objects.ministry import Ministry
from domain.value_objects.nor import NOR
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory


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
def db_cv_uuid_fixture(cv_metadata_completed) -> UUID:
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    return cv_metadata_completed.id


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
    assertContains(response, "js/drawer.js")


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


@pytest.mark.parametrize(
    "filter_test_case",
    [
        {
            "filters": {"filter-location": "75"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": ["Responsable des ressources humaines"],
        },
        {
            "filters": {"filter-location": "75", "filter-category": "a"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": [
                "Technicien informatique",
                "Responsable des ressources humaines",
            ],
        },
    ],
)
@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_full_page_load_with_filter_params_returns_filtered_results(
    mock_execute, client, db, filter_test_case, db_cv_uuid
):
    # Create Concours models using the factory with valid data
    concours_paris_model = ConcoursFactory.create_model(
        corps="Chef de projet transformation numérique",
        grade="Attaché principal",
        category=Category.A,
        open_position_number=5,
    )

    concours_lyon_model = ConcoursFactory.create_model(
        corps="Responsable des ressources humaines",
        grade="Attaché",
        category=Category.A,
        open_position_number=3,
    )

    concours_tech_model = ConcoursFactory.create_model(
        corps="Technicien informatique",
        grade="Technicien",
        category=Category.B,
        open_position_number=2,
    )

    # Convert models to entities
    concours_paris = concours_paris_model.to_entity()
    concours_lyon = concours_lyon_model.to_entity()
    concours_tech = concours_tech_model.to_entity()

    # Mock the usecase to return filtered results based on the test case
    all_opportunities = [
        (concours_paris, 0.9),
        (concours_lyon, 0.8),
        (concours_tech, 0.7),
    ]

    # Filter opportunities based on the test filters
    filters = filter_test_case["filters"]
    filtered_opportunities = []

    for opportunity, score in all_opportunities:
        include = True

        # Filter by location (simulated - in real app this would be done by the usecase)
        if "filter-location" in filters and filters["filter-location"]:
            location_filter = filters["filter-location"]
            # Map concours to departments for testing
            concours_locations = {
                "Chef de projet transformation numérique": "75",
                "Responsable des ressources humaines": "69",
                "Technicien informatique": "13",
            }
            if concours_locations.get(opportunity.corps) != location_filter:
                include = False

        # Filter by category
        if "filter-category" in filters and filters["filter-category"]:
            category_filter = filters["filter-category"]
            category_mapping = {"a": Category.A, "b": Category.B}
            if opportunity.category != category_mapping.get(category_filter):
                include = False

        if include:
            filtered_opportunities.append((opportunity, score))

    mock_execute.return_value = filtered_opportunities

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        filter_test_case["filters"],
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    for title in filter_test_case["expected_titles"]:
        assertContains(response, title)
    for title in filter_test_case["excluded_titles"]:
        assertNotContains(response, title)


# TODO - add vectorized offers in test
@pytest.mark.parametrize(
    "filter_test_case",
    [
        {
            "filters": {"filter-location": "75"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": ["Responsable des ressources humaines"],
        },
        {
            "filters": {"filter-location": "69"},
            "expected_titles": ["Responsable des ressources humaines"],
            "excluded_titles": ["Chef de projet transformation numérique"],
        },
        {
            "filters": {"filter-category": "b"},
            "expected_titles": ["Technicien informatique"],
            "excluded_titles": ["Chef de projet transformation numérique"],
        },
        {
            "filters": {"filter-location": "75", "filter-category": "a"},
            "expected_titles": ["Chef de projet transformation numérique"],
            "excluded_titles": [
                "Technicien informatique",
                "Responsable des ressources humaines",
            ],
        },
        {
            "filters": {"filter-location": "33"},
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
@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_filter_returns_filtered_results(
    mock_execute, client, db, filter_test_case, db_cv_uuid
):
    # Create Concours models using the factory with valid data
    concours_paris_model = ConcoursFactory.create_model(
        corps="Chef de projet transformation numérique",
        grade="Attaché principal",
        category=Category.A,
        open_position_number=5,
    )

    concours_lyon_model = ConcoursFactory.create_model(
        corps="Responsable des ressources humaines",
        grade="Attaché",
        category=Category.A,
        open_position_number=3,
    )

    concours_tech_model = ConcoursFactory.create_model(
        corps="Technicien informatique",
        grade="Technicien",
        category=Category.B,
        open_position_number=2,
    )

    # Convert models to entities
    concours_paris = concours_paris_model.to_entity()
    concours_lyon = concours_lyon_model.to_entity()
    concours_tech = concours_tech_model.to_entity()

    # Mock the usecase to return filtered results based on the test case
    all_opportunities = [
        (concours_paris, 0.9),
        (concours_lyon, 0.8),
        (concours_tech, 0.7),
    ]

    # Filter opportunities based on the test filters
    filters = filter_test_case["filters"]
    filtered_opportunities = []

    for opportunity, score in all_opportunities:
        include = True

        # Filter by location (simulated - in real app this would be done by the usecase)
        if "filter-location" in filters and filters["filter-location"]:
            location_filter = filters["filter-location"]
            # Map concours to departments for testing
            concours_locations = {
                "Chef de projet transformation numérique": "75",
                "Responsable des ressources humaines": "69",
                "Technicien informatique": "13",
            }
            if concours_locations.get(opportunity.corps) != location_filter:
                include = False

        # Filter by category
        if "filter-category" in filters and filters["filter-category"]:
            category_filter = filters["filter-category"]
            category_mapping = {"a": Category.A, "b": Category.B}
            if opportunity.category != category_mapping.get(category_filter):
                include = False

        if include:
            filtered_opportunities.append((opportunity, score))

    mock_execute.return_value = filtered_opportunities

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": db_cv_uuid}),
        filter_test_case["filters"],
        HTTP_HX_REQUEST="true",
        HTTP_HX_TARGET="results-zone",
    )
    assert response.status_code == HTTPStatus.OK

    if filter_test_case["expected_titles"]:
        assertTemplateUsed(response, "candidate/components/_results_list.html")
    else:
        assertTemplateUsed(response, "candidate/components/_no_results_content.html")

    for title in filter_test_case["expected_titles"]:
        assertContains(response, title)
    for title in filter_test_case["excluded_titles"]:
        assertNotContains(response, title)


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
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = [(OfferFactory.create_entity(title="Poste ciblé"), 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id}),
        HTTP_HX_REQUEST="true",
        HTTP_HX_TARGET="results-zone",
    )
    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_results_list.html")
    assertContains(response, "Poste ciblé")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_filter_bar_renders_tooltips(
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = [(OfferFactory.create_entity(title="Poste test"), 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id})
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, 'role="tooltip"', count=6)
    assertContains(response, "fr-btn--tooltip", count=6)


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_processing_flow_pending_to_completed(
    mock_execute, client, db, cv_metadata_pending
):
    model = CVMetadataModel.from_entity(cv_metadata_pending)
    model.save()
    url = reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_pending.id})

    response_initial = client.get(url)
    assert response_initial.status_code == HTTPStatus.OK
    assertTemplateUsed(response_initial, "candidate/cv_processing.html")
    assertContains(
        response_initial,
        f'hx-trigger="every {settings.CV_PROCESSING_POLL_INTERVAL}s"',
    )

    response_poll = client.get(url, {"poll": "1"}, HTTP_HX_REQUEST="true")
    assert response_poll.status_code == HTTPStatus.NO_CONTENT
    assert response_poll["HX-Reswap"] == "none"

    model.status = CVStatus.COMPLETED.value
    model.save()
    mock_execute.return_value = [
        (OfferFactory.create_model(title="Test opportunity"), 0.9),
    ]
    response_completed = client.get(url, {"poll": "1"}, HTTP_HX_REQUEST="true")
    assert response_completed.status_code == HTTPStatus.OK
    assert response_completed["HX-Redirect"] == url


def test_cv_results_with_pending_cv_in_database_shows_processing(
    client, db, cv_metadata_pending
):
    CVMetadataModel.from_entity(cv_metadata_pending).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_pending.id})
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
    mock_execute, client, db, concours, cv_metadata_completed
):
    mock_execute.return_value = [(concours[0], 0.9)]
    CVMetadataModel.from_entity(cv_metadata_completed).save()

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_results.html")
    assertContains(response, "Offres et concours les plus pertinents")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_poll_pending_to_completed_transition(
    mock_execute, client, db, concours
):
    mock_execute.return_value = [(concours[0], 0.9)]
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.PENDING)
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


def test_cv_results_failed_status_redirects_with_error_message(client, db):
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.FAILED)
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


def test_cv_results_htmx_request_sets_redirect_header(client, db):
    cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.FAILED)
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
def test_cv_results_shows_no_results_when_empty(
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/cv_no_results.html")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_htmx_empty_opportunities_shows_no_results(
    mock_execute, client, db, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, "candidate/components/_no_results_content.html")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_no_results_includes_tally_iframe(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.TALLY_FORM_ID_NO_RESULTS = "test-no-results-form"
    mock_execute.return_value = []

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id}),
        HTTP_HX_REQUEST="true",
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-no-results-form")
    assertContains(response, f"cv_uuid={cv_metadata_completed.id}")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_with_results_includes_tally_modal(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()

    settings.TALLY_FORM_ID_RESULTS = "test-results-form"
    mock_execute.return_value = [(OfferFactory.create_entity(title="Poste test"), 0.9)]

    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id})
    )

    assert response.status_code == HTTPStatus.OK
    assertContains(response, "tally.so/embed/test-results-form")
    assertContains(response, f"cv_uuid={cv_metadata_completed.id}")
    assertContains(response, "tally-results-modal")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_pagination_default_page(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.CV_RESULTS_PER_PAGE = 2
    mock_execute.return_value = [
        (OfferFactory.create_entity(title=f"Opportunity {i}"), 0.9 - i * 0.01)
        for i in range(5)
    ]
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id})
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Opportunity 0")
    assertContains(response, "Opportunity 1")
    assertNotContains(response, "Opportunity 2")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_pagination_second_page(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.CV_RESULTS_PER_PAGE = 2
    mock_execute.return_value = [
        (OfferFactory.create_entity(title=f"Opportunity {i}"), 0.9 - i * 0.01)
        for i in range(5)
    ]
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id}),
        {"page": "2"},
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Opportunity 2")
    assertContains(response, "Opportunity 3")
    assertNotContains(response, "Opportunity 0")


@patch(
    "application.candidate.usecases.match_cv_to_opportunities.MatchCVToOpportunitiesUsecase.execute"
)
def test_cv_results_pagination_with_filters(
    mock_execute, client, db, settings, cv_metadata_completed
):
    CVMetadataModel.from_entity(cv_metadata_completed).save()
    settings.CV_RESULTS_PER_PAGE = 1
    mock_execute.return_value = [
        (
            OfferFactory.create_entity(title=f"Paris {i}", department="75"),
            0.9 - i * 0.01,
        )
        for i in range(3)
    ]
    response = client.get(
        reverse("candidate:cv_results", kwargs={"cv_uuid": cv_metadata_completed.id}),
        {"filter-location": "75", "page": "2"},
    )
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "Paris 1")
    assertNotContains(response, "Paris 0")
