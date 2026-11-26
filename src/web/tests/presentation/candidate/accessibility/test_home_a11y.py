import pytest
from playwright.sync_api import Page

from tests.utils.axe import assert_no_axe_violations


@pytest.mark.accessibility
class TestHomePageAccessibility:
    def test_home_page_has_no_violations(self, page: Page, live_server) -> None:
        page.goto(live_server.url)
        assert_no_axe_violations(page)
