import re
from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory


@pytest.mark.e2e
class TestResultsDrawer:
    def test_user_opens_offer_drawer_and_closes_it_with_close_button(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.build(title="Offre e2e drawer")
        OfferModel.from_entity(offer_entity).save()

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
            mock_execute.return_value = [(offer_entity, 0.9)]

            page.goto(f"{live_server.url}{results_url}")
            expect(page.get_by_test_id("cv-results")).to_be_visible()

            page.locator("[data-drawer-open]").first.click()

            drawer = page.get_by_test_id("opportunity-drawer")
            expect(drawer).to_be_visible()
            expect(drawer).to_contain_text("Offre e2e drawer")

            drawer.locator("[data-drawer-close]").click()
            expect(drawer).not_to_be_visible()

    def test_user_closes_drawer_with_browser_back_navigation(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.build(title="Offre e2e back-nav")
        OfferModel.from_entity(offer_entity).save()

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
            mock_execute.return_value = [(offer_entity, 0.9)]

            page.goto(f"{live_server.url}{results_url}")
            expect(page.get_by_test_id("cv-results")).to_be_visible()

            page.locator("[data-drawer-open]").first.click()
            drawer = page.get_by_test_id("opportunity-drawer")
            expect(drawer).to_be_visible()

            page.go_back()

            expect(drawer).not_to_be_visible()
            expect(page).to_have_url(re.compile(re.escape(results_url) + r"/?$"))

    def test_user_opens_concours_drawer_and_closes_it_with_close_button(
        self, page: Page, live_server, transactional_db
    ) -> None:
        concours_model = ConcoursFactory.create(
            corps="Corps e2e drawer", grade="Grade e2e drawer"
        )
        concours_entity = concours_model.to_entity()

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
            mock_execute.return_value = [(concours_entity, 0.9)]

            page.goto(f"{live_server.url}{results_url}")
            expect(page.get_by_test_id("cv-results")).to_be_visible()

            page.locator("[data-drawer-open]").first.click()

            drawer = page.get_by_test_id("opportunity-drawer")
            expect(drawer).to_be_visible()
            expect(drawer).to_contain_text("Corps e2e drawer")

            drawer.locator("[data-drawer-close]").click()
            expect(drawer).not_to_be_visible()
