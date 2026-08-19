import pytest

from tests.utils.pdf_test_utils import cv_pdf_path  # noqa F401


@pytest.fixture(scope="session")
def _fast_polling(settings) -> None:
    settings.CV_PROCESSING_POLL_INTERVAL = 1
