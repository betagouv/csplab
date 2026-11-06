import pytest
from axe_playwright_python.sync_playwright import Axe
from django.urls import reverse
from playwright.sync_api import Page


@pytest.mark.accessibility
class TestApiChangelogAccessibility:
    @pytest.mark.parametrize("query", ["", "?type=retire"])
    def test_page_has_no_violations(self, page: Page, live_server, query) -> None:
        page.goto(f"{live_server.url}{reverse('pages:api_changelog')}{query}")
        results = Axe().run(page)
        assert results.violations_count == 0, results.generate_report()
