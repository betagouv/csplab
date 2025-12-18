"""Accessibility tests for candidate app pages.

These tests check WCAG 2.1 AA compliance using axe-core.
DSFR components are assumed to be accessible as they are tested
by the design system team.
"""

# pyright: reportGeneralTypeIssues=false
# Type stubs for playwright.async_api are incomplete

import os
from unittest import skipUnless

from apps.shared.tests.e2e.testcases import AccessibilityTestCase, async_test


@skipUnless(
    os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes"),
    "E2E tests disabled. Set RUN_E2E_TESTS=1 to run.",
)
class HomePageAccessibilityTests(AccessibilityTestCase):
    """Accessibility tests for the homepage."""

    async def _open_page(self):
        """Navigate to homepage."""
        await self.navigate_to_view("candidate:home")

    @async_test
    async def test_homepage_accessibility(self):
        """Homepage meets WCAG 2.1 AA standards."""
        await self.lazy_loading(self._open_page)
        results = await self.check_accessibility("homepage", strict=True)
        self.assertEqual(results.violations_count, 0)


@skipUnless(
    os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes"),
    "E2E tests disabled. Set RUN_E2E_TESTS=1 to run.",
)
class UploadFormAccessibilityTests(AccessibilityTestCase):
    """Accessibility tests for the CV upload form."""

    async def _open_page(self):
        """Navigate to upload page."""
        await self.navigate_to_view("candidate:cv_upload")

    @async_test
    async def test_upload_form_has_labels(self):
        """File input has proper label association."""
        await self.lazy_loading(self._open_page)

        # Check that file input has associated label
        file_input = self.page.locator('input[type="file"]')
        input_id = await file_input.get_attribute("id")

        if input_id:
            label = self.page.locator(f'label[for="{input_id}"]')
            label_count = await label.count()
            self.assertGreater(
                label_count,
                0,
                "File input should have an associated label",
            )

    @async_test
    async def test_upload_form_accessibility(self):
        """Upload form meets WCAG 2.1 AA standards."""
        await self.lazy_loading(self._open_page)
        results = await self.check_accessibility("upload_form", strict=True)
        self.assertEqual(results.violations_count, 0)

    @async_test
    async def test_form_has_submit_button(self):
        """Form has accessible submit button."""
        await self.lazy_loading(self._open_page)

        submit = self.page.locator('button[type="submit"]')
        submit_count = await submit.count()
        self.assertGreater(submit_count, 0, "Form should have a submit button")

        # Button should have accessible name
        button_text = await submit.first.inner_text()
        self.assertTrue(
            len(button_text.strip()) > 0,
            "Submit button should have visible text",
        )


@skipUnless(
    os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes"),
    "E2E tests disabled. Set RUN_E2E_TESTS=1 to run.",
)
class ResultsPageAccessibilityTests(AccessibilityTestCase):
    """Accessibility tests for the results page.

    Note: These tests require session data or mocked state.
    """

    @classmethod
    def setUpClass(cls):
        """Enable mocks for results page testing."""
        os.environ.setdefault("TYCHO_USE_MOCK_ALBERT", "true")
        os.environ.setdefault("TYCHO_USE_MOCK_OPENROUTER", "true")
        super().setUpClass()

    @async_test
    async def test_results_page_structure(self):
        """Results page has proper heading hierarchy."""
        # Results page requires a valid CV UUID - skip for now
        # This test would need to create a CV first or use a fixture
        self.skipTest("Results page requires CV UUID - needs integration test setup")

    @async_test
    async def test_results_page_accessibility(self):
        """Results page meets WCAG 2.1 AA standards."""
        # Results page requires a valid CV UUID - skip for now
        self.skipTest("Results page requires CV UUID - needs integration test setup")


@skipUnless(
    os.environ.get("RUN_E2E_TESTS", "").lower() in ("1", "true", "yes"),
    "E2E tests disabled. Set RUN_E2E_TESTS=1 to run.",
)
class NavigationAccessibilityTests(AccessibilityTestCase):
    """Accessibility tests for navigation and keyboard access."""

    async def _open_page(self):
        """Navigate to homepage."""
        await self.navigate_to_view("candidate:home")

    @async_test
    async def test_skip_link_present(self):
        """Page has skip to main content link."""
        await self.lazy_loading(self._open_page)

        # DSFR should provide skip link
        skip_link = self.page.locator('a[href="#main"], .fr-skiplinks')
        skip_count = await skip_link.count()
        self.assertGreater(
            skip_count,
            0,
            "Page should have skip navigation link",
        )

    @async_test
    async def test_main_landmark_present(self):
        """Page has main landmark."""
        await self.lazy_loading(self._open_page)

        main = self.page.locator("main, [role='main']")
        main_count = await main.count()
        self.assertGreater(main_count, 0, "Page should have main landmark")

    @async_test
    async def test_keyboard_navigation(self):
        """Interactive elements are keyboard accessible."""
        await self.lazy_loading(self._open_page)

        # Tab to first focusable element
        await self.page.keyboard.press("Tab")

        # Should have focus somewhere
        focused = await self.page.evaluate("document.activeElement.tagName")
        self.assertNotEqual(focused, "BODY", "Tab should move focus to an element")
