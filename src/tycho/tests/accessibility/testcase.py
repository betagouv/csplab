"""Base test classes for accessibility testing with Playwright and axe-core."""

import asyncio
import warnings
from functools import wraps
from typing import Any, Callable, ClassVar

from axe_playwright_python.async_playwright import Axe
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


def async_test(func: Callable[..., Any]) -> Callable[..., Any]:
    """Transform an async test method into a synchronous one for pytest/unittest."""

    @wraps(func)
    def wrapper(self: "FunctionalTestCase") -> Any:
        return self.loop.run_until_complete(func(self))

    return wrapper


@tag("functional")
class FunctionalTestCase(StaticLiveServerTestCase):
    """Base class for functional tests with Playwright."""

    loop: ClassVar[asyncio.AbstractEventLoop]
    playwright: ClassVar[Playwright]
    browser: ClassVar[Browser]
    context: BrowserContext
    page: Page

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class fixtures for Playwright browser."""
        super().setUpClass()
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.loop.run_until_complete(cls._async_setup())

    @classmethod
    async def _async_setup(cls) -> None:
        cls.playwright = await async_playwright().start()
        headless = getattr(settings, "HEADLESS_FUNCTIONAL_TESTS", True)
        slow_mo = 100 if headless else 1500
        cls.browser = await cls.playwright.chromium.launch(
            headless=headless,
            slow_mo=slow_mo,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class fixtures for Playwright browser."""
        cls.loop.run_until_complete(cls._async_teardown())
        cls.loop.close()
        super().tearDownClass()

    @classmethod
    async def _async_teardown(cls) -> None:
        if cls.browser:
            await cls.browser.close()
        if cls.playwright:
            await cls.playwright.stop()

    def setUp(self) -> None:
        """Set up test fixtures for each test."""
        super().setUp()
        self.loop.run_until_complete(self._async_test_setup())

    async def _async_test_setup(self) -> None:
        self.context = await self.browser.new_context()
        self.page: Page = await self.context.new_page()

    def tearDown(self) -> None:
        """Tear down test fixtures after each test."""
        self.loop.run_until_complete(self._async_test_teardown())
        super().tearDown()

    async def _async_test_teardown(self) -> None:
        if hasattr(self, "context") and self.context:
            await self.context.close()

    async def navigate_to_url(self, url_path: str) -> None:
        """Navigate to a URL path relative to the live server."""
        await self.page.goto(self.live_server_url + url_path)
        await self.page.wait_for_load_state("domcontentloaded")


@tag("accessibility")
class AccessibilityTestCase(FunctionalTestCase):
    """Base class for accessibility tests with Playwright and axe-core.

    Uses lazy loading to share page state between tests in the same class.
    """

    common_page: ClassVar[Page | None] = None
    axe: Axe | None = None

    async def lazy_loading(self, navigation_method: Callable[..., Any]) -> None:
        """Load page lazily, sharing it between tests of the same class."""
        if self.__class__.common_page is None:
            await navigation_method()
            self.__class__.common_page = self.page
        else:
            self.page = self.__class__.common_page

    def tearDown(self) -> None:
        """Skip teardown for shared page between tests."""
        if hasattr(self, "page") and self.page is self.__class__.common_page:
            pass
        else:
            super().tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up shared page at the end of all tests."""
        if hasattr(cls, "common_page") and cls.common_page is not None:
            if hasattr(cls.common_page, "context") and cls.common_page.context:
                cls.loop.run_until_complete(cls.common_page.context.close())
        super().tearDownClass()

    async def check_accessibility(
        self,
        page_name: str = "page",
        *,
        strict: bool = False,
        options: dict[str, Any] | None = None,
    ) -> Any:
        """Check accessibility of the current page using axe-core."""
        if options is None:
            options = {
                "exclude": [
                    ["nav[aria-label='Accès rapide']"],
                    ["header[role='banner']"],
                    ["nav[role='navigation']"],
                    ["footer[role='contentinfo']"],
                ]
            }

        if not hasattr(self, "axe") or self.axe is None:
            self.axe = Axe()

        try:
            results = await self.axe.run(self.page, options=options)
        except Exception:
            self.axe = Axe()
            results = await self.axe.run(self.page, options=options)

        violations_count = results.violations_count
        if violations_count > 0:
            violation_message = results.generate_report()

            if strict:
                self.assertEqual(violations_count, 0, violation_message)
            else:
                warnings.warn(
                    f"\n{'=' * 100}\n"
                    f"\nACCESSIBILITY WARNING [{page_name}]: "
                    f"{violations_count} violation(s) detected\n"
                    f"{'=' * 100}\n"
                    f"{violation_message}",
                    UserWarning,
                    stacklevel=2,
                )

        return results

    async def check_has_title(self, page_name: str = "page") -> str:
        """Assert the page has a non-empty title."""
        title = await self.page.title()
        self.assertTrue(len(title) > 0, f"{page_name}: Page title should not be empty")
        return title

    async def check_has_main(self, page_name: str = "page") -> int:
        """Assert the page has at least one <main> element."""
        main_count = await self.page.locator("main").count()
        self.assertGreaterEqual(
            main_count, 1, f"{page_name}: Page should have a <main> element"
        )
        return main_count

    async def check_has_h1(self, page_name: str = "page") -> int:
        """Assert the page has at least one <h1> heading."""
        h1_count = await self.page.locator("h1").count()
        self.assertGreaterEqual(
            h1_count, 1, f"{page_name}: Page should have at least one h1"
        )
        return h1_count

    async def check_page_structure(self, page_name: str = "page") -> None:
        """Run all structure checks: title, main, h1."""
        await self.check_has_title(page_name)
        await self.check_has_main(page_name)
        await self.check_has_h1(page_name)
