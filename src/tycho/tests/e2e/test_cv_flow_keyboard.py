import re
from pathlib import Path
from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.cv_metadata_factory import CVMetadataFactory
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

    def test_focus_returns_to_trigger_after_filter_then_drawer_escape(
        self,
        page: Page,
        live_server,
        transactional_db,
    ) -> None:
        offer_a = OfferFactory.build(title="Offre alpha kbd", category=Category.A)
        offer_b = OfferFactory.build(title="Offre beta kbd", category=Category.B)
        OfferModel.from_entity(offer_a).save()
        OfferModel.from_entity(offer_b).save()

        cv_metadata = CVMetadataFactory.build(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        def fake_execute(*, cv_metadata, filters, limit):
            if filters and "category" in filters:
                return [(offer_a, 0.9)]
            return [(offer_a, 0.9), (offer_b, 0.8)]

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute",
            side_effect=fake_execute,
        ):
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
