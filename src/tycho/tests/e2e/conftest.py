import os
from pathlib import Path

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

from tests.utils.pdf_test_utils import create_minimal_valid_pdf


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "locale": "fr-FR",
    }


@pytest.fixture(autouse=True)
def _fast_polling(settings) -> None:
    settings.CV_PROCESSING_POLL_INTERVAL = 1


@pytest.fixture
def cv_pdf_path(tmp_path: Path) -> Path:
    pdf_file = tmp_path / "cv.pdf"
    pdf_file.write_bytes(create_minimal_valid_pdf())
    return pdf_file
