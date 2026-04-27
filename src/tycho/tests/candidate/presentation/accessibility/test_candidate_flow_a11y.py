from unittest.mock import patch

import pytest
from axe_playwright_python.sync_playwright import Axe
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory

AXE_OPTIONS = {
    "runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]},
    "resultTypes": ["violations"],
}


def _assert_no_violations(axe_results) -> None:
    violations = axe_results.response.get("violations", [])
    assert violations == [], f"axe found {len(violations)} violation(s):\n" + "\n".join(
        f"- [{v['id']}] {v['help']}" for v in violations
    )


@pytest.mark.accessibility
class TestCandidateFlowAccessibility:
    def test_upload_page_has_no_axe_violations(
        self, page: Page, live_server, db
    ) -> None:
        page.goto(f"{live_server.url}{reverse('candidate:cv_upload')}")
        expect(page.get_by_role("heading", name="Importez votre CV")).to_be_visible()

        _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))

    def test_processing_page_has_no_axe_violations(
        self, page: Page, live_server, transactional_db
    ) -> None:
        cv_metadata = CVMetadataFactory.build(status=CVStatus.PENDING)
        CVMetadataModel.from_entity(cv_metadata).save()

        page.goto(
            f"{live_server.url}"
            f"{reverse('candidate:cv_results', kwargs={'cv_uuid': cv_metadata.id})}"
        )
        expect(
            page.get_by_role("heading", name="Analyse de votre CV en cours...")
        ).to_be_visible()

        _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))

    def test_results_page_has_no_axe_violations(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.build(title="Offre a11y")
        OfferModel.from_entity(offer_entity).save()
        cv_metadata = CVMetadataFactory.build(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute"
        ) as mock_execute:
            mock_execute.return_value = [(offer_entity, 0.9)]

            page.goto(
                f"{live_server.url}"
                f"{reverse('candidate:cv_results', kwargs={'cv_uuid': cv_metadata.id})}"
            )
            expect(
                page.get_by_role(
                    "heading", name="Offres et concours les plus pertinents"
                )
            ).to_be_visible()

            _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))

    def test_open_drawer_has_no_axe_violations(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.build(title="Offre drawer a11y")
        OfferModel.from_entity(offer_entity).save()
        cv_metadata = CVMetadataFactory.build(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute"
        ) as mock_execute:
            mock_execute.return_value = [(offer_entity, 0.9)]

            page.goto(
                f"{live_server.url}"
                f"{reverse('candidate:cv_results', kwargs={'cv_uuid': cv_metadata.id})}"
            )
            page.locator("[data-drawer-open]").first.click()
            expect(page.locator("dialog[data-drawer][open]")).to_be_visible()

            _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))
