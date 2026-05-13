import os

import pytest
from django.db import connections

from tests.utils.pdf_test_utils import cv_pdf_path  # noqa F401

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(autouse=True)
def close_worker_thread_connections():
    # Override the async version from shared_fixtures to avoid event loop
    # conflicts with Playwright, which manages its own event loop.
    yield
    connections.close_all()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "locale": "fr-FR",
    }


@pytest.fixture(scope="session")
def _fast_polling(settings) -> None:
    settings.CV_PROCESSING_POLL_INTERVAL = 1
