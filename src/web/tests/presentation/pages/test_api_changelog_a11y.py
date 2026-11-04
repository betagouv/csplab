import pytest
from axe_playwright_python.sync_playwright import Axe
from django.urls import reverse
from playwright.sync_api import Page


@pytest.mark.accessibility
class TestApiChangelogAccessibility:
    def test_page_has_no_violations(self, page: Page, live_server) -> None:
        page.goto(f"{live_server.url}{reverse('pages:api_changelog')}?type=retire")
        results = Axe().run(page)
        assert results.violations_count == 0, results.generate_report()
