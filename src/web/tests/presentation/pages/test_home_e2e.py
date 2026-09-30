import pytest
from playwright.sync_api import ConsoleMessage, Page, expect


@pytest.mark.e2e
class TestHomeNoticeE2E:
    def test_close_button_removes_notice(self, page: Page, live_server) -> None:
        csp_violations: list[str] = []

        def collect_csp_violations(message: ConsoleMessage) -> None:
            if "Content Security Policy" in message.text:
                csp_violations.append(message.text)

        page.on("console", collect_csp_violations)
        page.goto(live_server.url)
        notice = page.locator(".csplab-notice")
        expect(notice).to_be_visible()

        notice.get_by_role("button", name="Masquer le message").click()

        expect(notice).to_have_count(0)
        assert csp_violations == []
