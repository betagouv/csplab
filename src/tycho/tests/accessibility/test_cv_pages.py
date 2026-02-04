"""Accessibility tests for CV pages that require data."""

from typing import ClassVar

from django.test import tag

from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel
from tests.accessibility.testcase import AccessibilityTestCase, async_test
from tests.factories.cv_factories import CVMetadataModelFactory


@tag("accessibility")
class TestCVPagesAccessibility(AccessibilityTestCase):
    """Accessibility tests for CV pages that require data."""

    cv_uuid: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        """Create CV test data before running tests."""
        super().setUpClass()
        cv_metadata = CVMetadataModelFactory.create()
        cls.cv_uuid = str(cv_metadata.id)

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up CV test data."""
        CVMetadataModel.objects.filter(id=cls.cv_uuid).delete()
        super().tearDownClass()

    @async_test
    async def test_cv_processing_page_accessibility(self) -> None:
        """Verify CV processing page has no accessibility violations."""
        url = f"{self.live_server_url}/candidate/cv/{self.cv_uuid}/processing/"
        await self.page.goto(url)
        await self.page.wait_for_load_state("domcontentloaded")
        await self.check_accessibility(page_name="CV Processing", strict=True)

    @async_test
    async def test_cv_results_page_accessibility(self) -> None:
        """Verify CV results page has no accessibility violations."""
        url = f"{self.live_server_url}/candidate/cv/{self.cv_uuid}/results/"
        await self.page.goto(url)
        await self.page.wait_for_load_state("domcontentloaded")
        await self.check_accessibility(page_name="CV Results", strict=True)
