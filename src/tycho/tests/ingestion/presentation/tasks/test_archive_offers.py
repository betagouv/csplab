from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from huey.api import PeriodicTask

from presentation.ingestion.tasks import archive_offers, archive_offers_periodic


@pytest.fixture
def usecase():
    mock_usecase = MagicMock()
    mock_container = MagicMock()
    mock_container.archive_offers_usecase.return_value = mock_usecase
    with patch(
        "presentation.ingestion.tasks.create_ingestion_container",
        return_value=mock_container,
    ):
        yield mock_usecase


def test_periodic_task_does_not_call_usecase(usecase):
    assert issubclass(archive_offers_periodic.task_class, PeriodicTask)
    archive_offers_periodic.call_local()
    usecase.assert_not_called()


def test_task_calls_usecase(usecase):
    updated_after = datetime(2026, 1, 1)
    archive_offers.call_local(updated_after=updated_after, updated_before=None)
    usecase.execute.assert_called_once_with(updated_after)
