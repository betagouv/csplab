from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.cv_metadata_factory import CVMetadataFactory


@pytest.mark.e2e
class TestResultsEmptyAndFailedStates:
    def test_user_sees_no_results_state_when_matching_returns_empty(
        self, page: Page, live_server, transactional_db
    ) -> None:
        cv_metadata = CVMetadataFactory.build(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute"
        ) as mock_execute:
            mock_execute.return_value = []

            page.goto(f"{live_server.url}{results_url}")

            expect(
                page.get_by_text(
                    "nous n'avons pas trouvé d'opportunité",
                    exact=False,
                )
            ).to_be_visible()
            expect(page.get_by_test_id("cv-results")).not_to_be_visible()

    def test_user_is_redirected_to_upload_when_cv_status_is_failed(
        self, page: Page, live_server, transactional_db
    ) -> None:
        cv_metadata = CVMetadataFactory.build(
            status=CVStatus.FAILED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )
        upload_url = reverse("candidate:cv_upload")

        page.goto(f"{live_server.url}{results_url}")

        expect(page).to_have_url(f"{live_server.url}{upload_url}")
        expect(
            page.get_by_text(
                "Une erreur est survenue lors du traitement",
                exact=False,
            )
        ).to_be_visible()
