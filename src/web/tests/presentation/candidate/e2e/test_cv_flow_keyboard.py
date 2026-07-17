import re
from pathlib import Path
from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect
from referentiel.value_objects.category import Category

from domain.candidate.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.factories.candidate.cv_metadata_factory import CVMetadataFactory
from infrastructure.factories.referentiel.offer_factory import OfferFactory
from infrastructure.mappers.offer_mapper import OfferMapper


@pytest.mark.e2e
class TestCandidateFlowKeyboard:
    @patch(
        "application.candidate.usecases.match_cv_to_opportunities."
        "MatchCVToOpportunitiesUsecase.execute"
    )
    def test_user_completes_full_flow_with_keyboard_only(
        self,
        mock_execute,
        page: Page,
        live_server,
        cv_pdf_path: Path,
        transactional_db,
    ) -> None:
        offer_entity = OfferMapper().to_domain(
            OfferFactory.create_model(title="Offre keyboard")
        )
        mock_execute.return_value = [((offer_entity, []), 0.9)]

        # 1. Upload page: select file, submit via keyboard (Enter on submit button)
        page.goto(f"{live_server.url}/candidate/cv-upload")
        form = page.get_by_test_id("cv-upload-form")
        form.locator("input[data-file-input]").set_input_files(str(cv_pdf_path))

        submit_btn = form.locator('button[type="submit"]:visible')
        submit_btn.focus()
        expect(submit_btn).to_be_focused()
        page.keyboard.press("Enter")

        # 2. Processing page reached
        expect(page).to_have_url(re.compile(r"/candidate/cv/[0-9a-f-]+/results"))
        expect(page.get_by_test_id("cv-processing")).to_be_visible()

        match = re.search(r"/candidate/cv/([0-9a-f-]+)/results", page.url)
        assert match is not None
        cv_uuid = match.group(1)

        # 3. Flip CV to COMPLETED so polling renders results
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

    @patch(
        "application.candidate.usecases.match_cv_to_opportunities."
        "MatchCVToOpportunitiesUsecase.execute"
    )
    def test_focus_returns_to_trigger_after_filter_then_drawer_escape(
        self,
        mock_execute,
        page: Page,
        live_server,
        transactional_db,
    ) -> None:
        offer_a = OfferMapper().to_domain(
            OfferFactory.create_model(title="Offre alpha kbd", category=Category.A)
        )
        offer_b = OfferMapper().to_domain(
            OfferFactory.create_model(title="Offre beta kbd", category=Category.B)
        )

        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        def fake_execute(*, cv_metadata, filters, limit):
            if filters and "category" in filters:
                return [((offer_a, []), 0.9)]
            return [((offer_a, []), 0.9), ((offer_b, []), 0.8)]

        mock_execute.side_effect = fake_execute

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}
        )

        page.goto(f"{live_server.url}{results_url}")
        results = page.get_by_test_id("cv-results")
        expect(results).to_be_visible()

        page.locator("label:has(#desktop-filter-category-a)").click()
        expect(page).to_have_url(re.compile(r"filter-category=a"))
        expect(results).not_to_contain_text("Offre beta kbd")

        trigger = page.locator("[data-drawer-open]").first
        trigger.focus()
        page.keyboard.press("Enter")

        drawer = page.get_by_test_id("opportunity-drawer")
        expect(drawer).to_be_visible()

        page.keyboard.press("Escape")
        expect(drawer).not_to_be_visible()
        expect(trigger).to_be_focused()
