"""Base test cases for E2E and accessibility testing with Playwright."""

from __future__ import annotations

import asyncio
import re

from axe_playwright_python.async_playwright import Axe
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from django.urls import reverse
from playwright.async_api import async_playwright


def async_test(func):
    """Decorator to run async test methods in Django TestCase."""

    def wrapper(self):
        return self.loop.run_until_complete(func(self))

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@tag("e2e")
class PlaywrightTestCase(StaticLiveServerTestCase):
    """Base class for E2E tests with Playwright.

    Provides async browser automation with proper setup/teardown.
    Uses Django's StaticLiveServerTestCase for serving static files.

    Usage:
        class MyTests(PlaywrightTestCase):
            @async_test
            async def test_page_loads(self):
                await self.navigate_to_view("myapp:home")
                await expect(self.page).to_have_title("Home")
    """

    @classmethod
    def setUpClass(cls):
        """Set up browser instance shared across all tests in class."""
        super().setUpClass()
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.loop.run_until_complete(cls._async_setup())

    @classmethod
    async def _async_setup(cls):
        """Launch Playwright and browser."""
        cls.playwright = await async_playwright().start()
        headless = getattr(settings, "E2E_HEADLESS", True)
        cls.browser = await cls.playwright.chromium.launch(
            headless=headless,
            slow_mo=50 if headless else 300,
        )

    @classmethod
    def tearDownClass(cls):
        """Close browser and Playwright."""
        cls.loop.run_until_complete(cls._async_teardown())
        cls.loop.close()
        super().tearDownClass()

    @classmethod
    async def _async_teardown(cls):
        """Clean up browser resources."""
        if hasattr(cls, "browser") and cls.browser:
            await cls.browser.close()
        if hasattr(cls, "playwright") and cls.playwright:
            await cls.playwright.stop()

    def setUp(self):
        """Create fresh browser context and page for each test."""
        super().setUp()
        self.loop.run_until_complete(self._async_test_setup())

    async def _async_test_setup(self):
        """Create isolated browser context for test."""
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    def tearDown(self):
        """Close browser context after each test."""
        self.loop.run_until_complete(self._async_test_teardown())
        super().tearDown()

    async def _async_test_teardown(self):
        """Clean up browser context."""
        if hasattr(self, "context") and self.context:
            await self.context.close()

    # --- Navigation helpers ---

    async def navigate_to(self, url_path: str):
        """Navigate to a relative URL path.

        Args:
            url_path: Path starting with /
        """
        await self.page.goto(self.live_server_url + url_path)
        await self.page.wait_for_load_state("domcontentloaded")

    async def navigate_to_view(self, viewname: str, **kwargs):
        """Navigate to a Django view by name.

        Args:
            viewname: Django URL name (e.g., "candidate:home")
            **kwargs: URL parameters
        """
        url = reverse(viewname, kwargs=kwargs if kwargs else None)
        await self.navigate_to(url)

    def url_pattern(self, viewname: str, kwargs: dict | None = None) -> re.Pattern:
        """Generate regex pattern for URL matching.

        Args:
            viewname: Django URL name
            kwargs: URL parameters

        Returns:
            Compiled regex pattern
        """
        url = reverse(viewname, kwargs=kwargs or {})
        return re.compile(rf"http://[^/]+{re.escape(url)}")

    async def wait_for_view(
        self, viewname: str, kwargs: dict | None = None, timeout: int = 30000
    ):
        """Wait for navigation to a specific Django view.

        Args:
            viewname: Django URL name
            kwargs: URL parameters
            timeout: Max wait time in milliseconds
        """
        pattern = self.url_pattern(viewname, kwargs)
        await self.page.wait_for_url(pattern, timeout=timeout)


@tag("e2e", "a11y")
class AccessibilityTestCase(PlaywrightTestCase):
    """Base class for accessibility tests with axe-core.

    Extends PlaywrightTestCase with axe-core integration for WCAG/RGAA compliance.
    Uses lazy_loading pattern to share page state between related a11y checks.

    Usage:
        class HomeA11yTests(AccessibilityTestCase):
            async def _open_page(self):
                await self.navigate_to_view("myapp:home")

            @async_test
            async def test_accessibility(self):
                await self.lazy_loading(self._open_page)
                await self.check_accessibility("home_page", strict=True)
    """

    _shared_page = None

    # Exclude common DSFR elements that are tested by the design system
    AXE_EXCLUDE = [
        ["[data-fr-js-modal]"],  # DSFR modals
    ]

    async def lazy_loading(self, navigation_method):
        """Share page between tests in same class for performance.

        Args:
            navigation_method: Async method that navigates to the page
        """
        if self.__class__._shared_page is None:
            await navigation_method()
            self.__class__._shared_page = self.page
        else:
            self.page = self.__class__._shared_page

    def tearDown(self):
        """Keep shared page open between tests."""
        if hasattr(self, "page") and self.page is self.__class__._shared_page:
            pass  # Don't close shared page
        else:
            super().tearDown()

    @classmethod
    def tearDownClass(cls):
        """Clean up shared page at end of all tests."""
        cls._shared_page = None
        super().tearDownClass()

    async def check_accessibility(
        self,
        page_name: str = "page",
        strict: bool = False,
        exclude: list | None = None,
    ):
        """Run axe-core accessibility check on current page.

        Args:
            page_name: Identifier for reports
            strict: If True, fail on any violations
            exclude: Additional selectors to exclude from analysis

        Returns:
            AxeResults object with violations info
        """
        axe = Axe()

        exclude_selectors = self.AXE_EXCLUDE + (exclude or [])
        options = {"exclude": exclude_selectors} if exclude_selectors else {}

        results = await axe.run(self.page, options=options)

        if results.violations_count > 0:
            report = results.generate_report()

            if strict:
                self.fail(
                    f"Accessibility violations on {page_name} "
                    f"({results.violations_count} issues):\n{report}"
                )

        return results
