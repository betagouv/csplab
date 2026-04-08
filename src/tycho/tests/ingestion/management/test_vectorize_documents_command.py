from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from domain.entities.document import DocumentType

VECTORIZE_LIMIT = 5

_CMD_MODULE = (
    "infrastructure.django_apps.ingestion.management.commands.vectorize_documents"
)


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
    with patch(f"{_CMD_MODULE}.vectorize_documents") as mock:
        yield mock


class TestVectorizeDocumentsCommand:
    def test_command_requires_type_argument(self, mock_container_factory):
        with pytest.raises(CommandError):
            call_command("vectorize_documents")

    def test_command_rejects_invalid_type(self, mock_container_factory):
        with pytest.raises(CommandError):
            call_command("vectorize_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type",
        [DocumentType.CONCOURS, DocumentType.OFFERS, DocumentType.CORPS],
    )
    def test_command_enqueues_task_with_correct_parameters(
        self,
        mock_task,
        document_type,
    ):
        args = ["vectorize_documents", "--type", document_type.value]

        call_command(*args)

        mock_task.assert_called_once_with(document_type)

    def test_command_logs(self, mock_task, mock_logger):
        call_command("vectorize_documents", "--type", DocumentType.OFFERS.value)

        mock_logger.info.assert_any_call(
            "Enqueuing vectorization task for %s...",
            DocumentType.OFFERS.value,
        )
        mock_logger.info.assert_any_call("✅ Task enqueued successfully.")
        assert mock_logger.info.call_count == 2  # noqa
