import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page


@pytest.mark.accessibility
class TestHomePageAccessibility:
    def test_home_page_has_no_violations(self, page: Page, live_server) -> None:
        page.goto(live_server.url)
        results = Axe().run(page)
        assert results.violations_count == 0, results.generate_report()
