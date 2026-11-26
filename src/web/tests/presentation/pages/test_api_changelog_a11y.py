import pytest
from django.urls import reverse
from playwright.sync_api import Page

from tests.utils.axe import assert_no_axe_violations


@pytest.mark.accessibility
class TestApiChangelogAccessibility:
    @pytest.mark.parametrize("query", ["", "?type=retire"])
    def test_page_has_no_violations(self, page: Page, live_server, query) -> None:
        page.goto(f"{live_server.url}{reverse('pages:api_changelog')}{query}")
        assert_no_axe_violations(page)
