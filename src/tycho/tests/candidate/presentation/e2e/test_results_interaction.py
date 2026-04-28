import re
from functools import partial
from unittest.mock import patch

import pytest
from django.urls import reverse
from playwright.sync_api import Page, expect

from domain.value_objects.category import Category
from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from infrastructure.django_apps.shared.models.offer import OfferModel
from tests.factories.concours_factory import ConcoursFactory
from tests.factories.cv_metadata_factory import CVMetadataFactory
from tests.factories.offer_factory import OfferFactory


def fake_execute_filter_by_category(offer_a, offer_b, *, cv_metadata, filters, limit):
    if filters and "category" in filters:
        return [(offer_a, 0.9)]
    return [(offer_a, 0.9), (offer_b, 0.8)]


def fake_execute_filter_by_category_and_versant(
    offer_a_fpe, offer_a_fpt, offer_b_fpe, *, cv_metadata, filters, limit
):
    has_cat = bool(filters and "category" in filters)
    has_versant = bool(filters and "verse" in filters)
    if has_cat and has_versant:
        return [(offer_a_fpe, 0.9)]
    if has_cat:
        return [(offer_a_fpe, 0.9), (offer_a_fpt, 0.85)]
    return [
        (offer_a_fpe, 0.9),
        (offer_a_fpt, 0.85),
        (offer_b_fpe, 0.8),
    ]


@pytest.mark.e2e
class TestResultsDrawer:
    def test_user_opens_offer_drawer_and_closes_it_with_close_button(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_entity = OfferFactory.create_entity(title="Offre e2e drawer")
        OfferModel.from_entity(offer_entity).save()

        cv_metadata = CVMetadataFactory.create_entity(
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
        offer_entity = OfferFactory.create_entity(title="Offre e2e back-nav")
        OfferModel.from_entity(offer_entity).save()

        cv_metadata = CVMetadataFactory.create_entity(
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
        concours_model = ConcoursFactory.create_model(
            corps="Corps e2e drawer", grade="Grade e2e drawer"
        )
        concours_entity = concours_model.to_entity()

        cv_metadata = CVMetadataFactory.create_entity(
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


@pytest.mark.e2e
class TestResultsFilters:
    def test_user_narrows_results_by_selecting_category_filter(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_a = OfferFactory.create_entity(title="Offre alpha", category=Category.A)
        offer_b = OfferFactory.create_entity(title="Offre beta", category=Category.B)
        OfferModel.from_entity(offer_a).save()
        OfferModel.from_entity(offer_b).save()

        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute",
            side_effect=partial(fake_execute_filter_by_category, offer_a, offer_b),
        ):
            page.goto(f"{live_server.url}{results_url}")
            results = page.get_by_test_id("cv-results")
            expect(results).to_contain_text("Offre alpha")
            expect(results).to_contain_text("Offre beta")

            page.locator("label:has(#desktop-filter-category-a)").click()

            expect(results).to_contain_text("Offre alpha")
            expect(results).not_to_contain_text("Offre beta")
            expect(page).to_have_url(re.compile(r"filter-category=a"))

    def test_user_lands_on_filtered_results_via_deep_link(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_a = OfferFactory.create_entity(
            title="Offre alpha deep", category=Category.A
        )
        offer_b = OfferFactory.create_entity(
            title="Offre beta deep", category=Category.B
        )
        OfferModel.from_entity(offer_a).save()
        OfferModel.from_entity(offer_b).save()

        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute",
            side_effect=partial(fake_execute_filter_by_category, offer_a, offer_b),
        ):
            page.goto(f"{live_server.url}{results_url}?filter-category=a")

            results = page.get_by_test_id("cv-results")
            expect(results).to_be_visible()
            expect(results).to_contain_text("Offre alpha deep")
            expect(results).not_to_contain_text("Offre beta deep")
            expect(page.locator("#desktop-filter-category-a")).to_be_checked()

    def test_user_combines_category_and_versant_filters(
        self, page: Page, live_server, transactional_db
    ) -> None:
        offer_a_fpe = OfferFactory.create_entity(
            title="Offre alpha FPE", category=Category.A
        )
        offer_a_fpt = OfferFactory.create_entity(
            title="Offre alpha FPT", category=Category.A
        )
        offer_b_fpe = OfferFactory.create_entity(
            title="Offre beta FPE", category=Category.B
        )
        OfferModel.from_entity(offer_a_fpe).save()
        OfferModel.from_entity(offer_a_fpt).save()
        OfferModel.from_entity(offer_b_fpe).save()

        cv_metadata = CVMetadataFactory.create_entity(
            status=CVStatus.COMPLETED, search_query="dev"
        )
        CVMetadataModel.from_entity(cv_metadata).save()

        results_url = reverse(
            "candidate:cv_results", kwargs={"cv_uuid": cv_metadata.id}
        )

        with patch(
            "application.candidate.usecases.match_cv_to_opportunities."
            "MatchCVToOpportunitiesUsecase.execute",
            side_effect=partial(
                fake_execute_filter_by_category_and_versant,
                offer_a_fpe,
                offer_a_fpt,
                offer_b_fpe,
            ),
        ):
            page.goto(f"{live_server.url}{results_url}")
            results = page.get_by_test_id("cv-results")
            expect(results).to_contain_text("Offre alpha FPE")
            expect(results).to_contain_text("Offre alpha FPT")
            expect(results).to_contain_text("Offre beta FPE")

            page.locator("label:has(#desktop-filter-category-a)").click()
            expect(page).to_have_url(re.compile(r"filter-category=a"))
            expect(results).not_to_contain_text("Offre beta FPE")

            page.locator("label:has(#desktop-filter-versant-FPE)").click()
            expect(page).to_have_url(re.compile(r"filter-versant=FPE"))
            expect(results).to_contain_text("Offre alpha FPE")
            expect(results).not_to_contain_text("Offre alpha FPT")
