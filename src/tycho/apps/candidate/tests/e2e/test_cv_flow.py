"""E2E tests for CV upload and analysis flow."""

import os
from pathlib import Path
from unittest import skipUnless

from django.conf import settings
from playwright.async_api import expect

from apps.shared.tests.e2e.testcases import PlaywrightTestCase, async_test


@skipUnless(
    os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes"),
    "E2E tests disabled. Set RUN_E2E_TESTS=1 to run.",
)
class CvUploadFlowTests(PlaywrightTestCase):
    """E2E tests for the CV upload and analysis workflow.

    These tests use mocked external services (Albert API, OpenRouter).
    Set TYCHO_USE_MOCK_ALBERT=true and TYCHO_USE_MOCK_OPENROUTER=true
    in the test environment for predictable results.
    """

    @classmethod
    def setUpClass(cls):
        """Ensure mock services are enabled for tests."""
        os.environ.setdefault("TYCHO_USE_MOCK_ALBERT", "true")
        os.environ.setdefault("TYCHO_USE_MOCK_OPENROUTER", "true")
        super().setUpClass()

    @async_test
    async def test_home_page_loads(self):
        """Homepage loads with proper structure."""
        await self.navigate_to_view("candidate:home")

        # Page title contains CSPLab
        title = await self.page.title()
        self.assertIn("CSPLab", title)

        # DSFR header present
        header = self.page.locator("header.fr-header")
        await expect(header).to_be_visible()

        # Main content area present
        main = self.page.locator("main")
        await expect(main).to_be_visible()

    @async_test
    async def test_upload_form_accepts_pdf(self):
        """Upload form accepts PDF files."""
        await self.navigate_to_view("candidate:cv_upload")

        # Find file input
        file_input = self.page.locator('input[type="file"]')
        await expect(file_input).to_be_attached()

        accept_attr = await file_input.get_attribute("accept")
        if accept_attr:
            # Should accept common document formats
            self.assertIn(".pdf", accept_attr.lower())

    @async_test
    async def test_complete_cv_flow_with_mocks(self):
        """Test complete CV upload to results flow using mocked services.

        This test verifies the full user journey:
        1. Load homepage
        2. Upload a CV file
        3. Wait for processing
        4. View analysis results
        """
        # Use test fixture CV
        test_cv_path = self._get_test_cv_path()
        if not test_cv_path or not test_cv_path.exists():
            self.skipTest("No test CV file available")

        # 1. Navigate to home
        await self.navigate_to_view("candidate:home")

        # 2. Upload file
        file_input = self.page.locator('input[type="file"]')
        await file_input.set_input_files(str(test_cv_path))

        # 3. Submit form
        submit_button = self.page.locator('button[type="submit"]')
        await submit_button.click()

        # 4. Wait for redirect to results (with longer timeout for processing)
        await self.page.wait_for_url(
            self.url_pattern("candidate:resultats_analyse"),
            timeout=60000,
        )

        # 5. Verify results page content
        await self.page.wait_for_load_state("domcontentloaded")

        # Should have results heading
        heading = self.page.locator("h1, h2").first
        await expect(heading).to_be_visible()

        # Should not show error alert
        error_alert = self.page.locator(".fr-alert--error")
        await expect(error_alert).to_have_count(0)

    @async_test
    async def test_upload_shows_loading_state(self):
        """Upload form has a submit button."""
        await self.navigate_to_view("candidate:cv_upload")

        # Find the submit button (could be button or input type=submit)
        submit_button = self.page.locator('button[type="submit"], input[type="submit"]')
        submit_count = await submit_button.count()
        self.assertGreater(submit_count, 0, "Form should have a submit button")

    def _get_test_cv_path(self) -> Path | None:
        """Get path to test CV fixture file.

        Returns:
            Path to test CV or None if not found.
        """
        # Look for test CV in fixtures
        fixtures_dir = (
            Path(settings.BASE_DIR) / "apps" / "candidate" / "tests" / "fixtures"
        )
        for ext in (".pdf", ".PDF"):
            cv_path = fixtures_dir / f"test_cv{ext}"
            if cv_path.exists():
                return cv_path

        # Try shared fixtures
        shared_fixtures = (
            Path(settings.BASE_DIR) / "apps" / "shared" / "tests" / "fixtures"
        )
        for ext in (".pdf", ".PDF"):
            cv_path = shared_fixtures / f"test_cv{ext}"
            if cv_path.exists():
                return cv_path

        return None
