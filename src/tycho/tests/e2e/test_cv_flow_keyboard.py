import re
from pathlib import Path
from unittest.mock import patch

import pytest
from playwright.sync_api import Page, expect

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.offer_factory import OfferFactory


@pytest.mark.e2e
class TestCandidateFlowKeyboard:
    def test_user_completes_full_flow_with_keyboard_only(
        self,
        page: Page,
        live_server,
        cv_pdf_path: Path,
        transactional_db,
    ) -> None:
        offer_entity = OfferFactory.build(title="Offre keyboard")
        OfferModel.from_entity(offer_entity).save()

        # 1. Upload page: select file, submit via keyboard (Enter on submit button)
        page.goto(f"{live_server.url}/candidate/cv-upload/")
        form = page.get_by_test_id("cv-upload-form")
        form.locator("input[data-file-input]").set_input_files(str(cv_pdf_path))

        submit_btn = form.locator('button[type="submit"]:visible')
        submit_btn.focus()
        expect(submit_btn).to_be_focused()
        page.keyboard.press("Enter")

        # 2. Processing page reached
        expect(page).to_have_url(re.compile(r"/candidate/cv/[0-9a-f-]+/results/"))
        expect(page.get_by_test_id("cv-processing")).to_be_visible()

        match = re.search(r"/candidate/cv/([0-9a-f-]+)/results/", page.url)
        assert match is not None
        cv_uuid = match.group(1)

        # 3. Flip CV to COMPLETED so polling renders results, mock matching usecase
        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute"
        ) as mock_execute:
            mock_execute.return_value = [(offer_entity, 0.9)]
            CVMetadataModel.objects.filter(id=cv_uuid).update(
                status=CVStatus.COMPLETED.value, search_query="dev"
            )

            results = page.get_by_test_id("cv-results")
            expect(results).to_be_visible(timeout=10_000)

            # 4. Open drawer with Enter on first offer link
            trigger = page.locator("[data-drawer-open]").first
            trigger.focus()
            page.keyboard.press("Enter")

            drawer = page.get_by_test_id("opportunity-drawer")
            expect(drawer).to_be_visible()
            expect(drawer.locator("[data-drawer-close]")).to_be_focused()

            # 5. Close drawer with Escape, focus returns to trigger
            page.keyboard.press("Escape")
            expect(drawer).not_to_be_visible()
            expect(trigger).to_be_focused()
