import re
from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory


@pytest.mark.e2e
class TestResultsPagination:
    def test_user_navigates_to_page_2_via_dsfr_pagination(
        self, page: Page, live_server, transactional_db, settings
    ) -> None:
        settings.CV_RESULTS_PER_PAGE = 3

        offers = [OfferFactory.build(title=f"Offre paginée {i}") for i in range(5)]
        for offer in offers:
            OfferModel.from_entity(offer).save()

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
            mock_execute.return_value = [
                (offer, 0.9 - i * 0.05) for i, offer in enumerate(offers)
            ]

            page.goto(f"{live_server.url}{results_url}")
            results = page.get_by_test_id("cv-results")
            expect(results).to_be_visible()
            expect(results).to_contain_text("Offre paginée 0")
            expect(results).not_to_contain_text("Offre paginée 4")

            page.locator('a.fr-pagination__link[title="Page 2"]').click()

            expect(page).to_have_url(re.compile(r"page=2"))
            expect(results).to_contain_text("Offre paginée 4")
            expect(results).not_to_contain_text("Offre paginée 0")
