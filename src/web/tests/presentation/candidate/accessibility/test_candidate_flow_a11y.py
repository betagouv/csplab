from unittest.mock import patch

import pytest
from axe_playwright_python.sync_playwright import Axe
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.candidate.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.mappers.offer_mapper import OfferMapper
from tests.factories.candidate.cv_metadata_factory import CVMetadataFactory
from tests.factories.referentiel.offer_factory import OfferFactory

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
        cv_metadata = CVMetadataFactory.create_entity(status=CVStatus.PENDING)
        CVMetadataModel.from_entity(cv_metadata).save()

        cv_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}
        )
        page.goto(f"{live_server.url}{cv_url}")
        expect(
            page.get_by_role("heading", name="Analyse de votre CV en cours...")
        ).to_be_visible()

        _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))

    @patch(
        "application.candidate.usecases.match_cv_to_opportunities."
        "MatchCVToOpportunitiesUsecase.execute"
    )
    def test_results_page_has_no_axe_violations(
        self, mock_execute, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.create_entity(title="Offre a11y")
        OfferMapper().from_domain(offer_entity).save()
        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()
        mock_execute.return_value = [(offer_entity, 0.9)]

        cv_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}
        )
        page.goto(f"{live_server.url}{cv_url}")
        expect(
            page.get_by_role("heading", name="Offres et concours les plus pertinents")
        ).to_be_visible()

        _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))

    @patch(
        "application.candidate.usecases.match_cv_to_opportunities."
        "MatchCVToOpportunitiesUsecase.execute"
    )
    def test_open_drawer_has_no_axe_violations(
        self, mock_execute, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.create_entity(title="Offre drawer a11y")
        OfferMapper().from_domain(offer_entity).save()
        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()
        mock_execute.return_value = [(offer_entity, 0.9)]

        cv_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.entity_id}
        )
        page.goto(f"{live_server.url}{cv_url}")
        page.locator("[data-drawer-open]").first.click()
        expect(page.locator("dialog[data-drawer][open]")).to_be_visible()

        _assert_no_violations(Axe().run(page, options=AXE_OPTIONS))
