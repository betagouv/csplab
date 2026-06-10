from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest


@contextmanager
def patch_ingestion_container(module_path: str):
    container = MagicMock()
    with patch(
        f"presentation.ingestion.views.{module_path}.create_ingestion_container",
        return_value=container,
    ):
        yield container


@pytest.fixture
def mock_offers_container():
    with patch_ingestion_container("offers") as container:
        yield container


@pytest.fixture
def mock_sources_container():
    with patch_ingestion_container("sources") as container:
        yield container


@pytest.fixture
def mock_metiers_container():
    with patch_ingestion_container("metiers") as container:
        yield container
