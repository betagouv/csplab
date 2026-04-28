import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "locale": "fr-FR",
    }


@pytest.fixture(autouse=True)
def _fast_polling(settings) -> None:
    settings.CV_PROCESSING_POLL_INTERVAL = 1
