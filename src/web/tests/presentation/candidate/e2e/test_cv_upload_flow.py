import re
from pathlib import Path
from unittest.mock import patch

import pytest
from playwright.sync_api import Page, expect

from domain.candidate.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.factories.referentiel.offer_factory import OfferFactory


@pytest.mark.e2e
class TestCVUploadFlow:
    @patch(
        "application.candidate.usecases.match_cv_to_opportunities."
        "MatchCVToOpportunitiesUsecase.execute"
    )
    def test_user_sees_results_after_processing_completes(
        self, mock_execute, page: Page, live_server, cv_pdf_path: Path, db
    ) -> None:
        mock_execute.return_value = [
            ((OfferFactory.create_entity(title="Offre e2e"), []), 0.9),
        ]

        page.goto(f"{live_server.url}/candidate/cv-upload")
        form = page.get_by_test_id("cv-upload-form")
        form.locator("input[data-file-input]").set_input_files(str(cv_pdf_path))
        form.locator('button[type="submit"]:visible').click()
        expect(page.get_by_test_id("cv-processing")).to_be_visible()

        match = re.search(r"/candidate/cv/([0-9a-f-]+)/results", page.url)
        assert match is not None
        cv_uuid = match.group(1)

        CVMetadataModel.objects.filter(id=cv_uuid).update(
            status=CVStatus.COMPLETED.value, search_query="dev"
        )
        expect(page.get_by_test_id("cv-results")).to_be_visible(timeout=10_000)
