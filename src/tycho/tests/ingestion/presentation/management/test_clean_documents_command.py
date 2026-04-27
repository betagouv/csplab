from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from domain.entities.document import DocumentType

_CMD_MODULE = "presentation.ingestion.management.commands.clean_documents"


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
    with patch(f"{_CMD_MODULE}.clean_documents") as mock:
        yield mock


class TestCleanDocumentsCommand:
    def test_command_requires_type_argument(self, mock_container_factory):
        with pytest.raises(CommandError):
            call_command("clean_documents")

    def test_command_rejects_invalid_type(self, mock_container_factory):
        with pytest.raises(CommandError):
            call_command("clean_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type",
        [
            DocumentType.CONCOURS,
            DocumentType.OFFERS,
            DocumentType.CORPS,
        ],
    )
    def test_command_enqueues_task_with_correct_parameters(
        self,
        mock_task,
        mock_logger,
        document_type,
    ):
        call_command("clean_documents", "--type", document_type.value)

        mock_task.assert_called_once_with(document_type)

        mock_logger.info.assert_any_call(
            "Enqueuing clean task for %s...",
            document_type.value,
        )
        mock_logger.info.assert_any_call("✅ Task enqueued successfully.")
        assert mock_logger.info.call_count == 2  # noqa
