from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command

_CMD_MODULE = "presentation.ingestion.management.commands.load_corps"


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def mock_container_factory(mock_logger):
    container = Mock()
    container.logger_service.return_value = mock_logger
    with patch(f"{_CMD_MODULE}.create_ingestion_container") as mock_factory:
        mock_factory.return_value = container
        yield mock_factory


@pytest.fixture
def mock_task(mock_container_factory):
    with patch(f"{_CMD_MODULE}.load_corps") as mock:
        yield mock


class TestLoadCorpsCommand:
    def test_command_calls_usecase_with_correct_parameters(
        self,
        mock_task,
        mock_logger,
    ):
        call_command("load_corps")

        mock_task.assert_called_once()
        mock_logger.info.assert_any_call(
            "Enqueuing load task for CORPS...",
        )
        mock_logger.info.assert_any_call("✅ Task enqueued successfully.")
        assert mock_logger.info.call_count == 2  # noqa
