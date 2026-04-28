import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
class TestE2EInfrastructure:
    def test_live_server_serves_home_page_in_browser(
        self, page: Page, live_server
    ) -> None:
        page.goto(live_server.url)
        expect(page).to_have_url(f"{live_server.url}/")
        expect(page.locator("body")).to_be_visible()
