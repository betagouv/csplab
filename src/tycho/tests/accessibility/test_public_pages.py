"""Accessibility tests for public static pages."""

from django.test import tag

from tests.accessibility.testcase import AccessibilityTestCase, async_test

PUBLIC_STATIC_PAGES = [
    ("/", "Home"),
    ("/candidate/", "Candidate Index"),
    ("/candidate/cv-upload/", "CV Upload"),
]


@tag("accessibility")
class TestPublicStaticPagesAccessibility(AccessibilityTestCase):
    """Run accessibility and structure checks on all public static pages."""

    @async_test
    async def test_all_pages_accessibility_and_structure(self) -> None:
        """Verify all pages pass accessibility and structure checks."""
        for url_path, page_name in PUBLIC_STATIC_PAGES:
            with self.subTest(page=page_name):
                await self.page.goto(self.live_server_url + url_path)
                await self.page.wait_for_load_state("domcontentloaded")

                await self.check_accessibility(page_name=page_name, strict=True)
                await self.check_page_structure(page_name)
