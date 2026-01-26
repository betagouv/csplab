"""Tests for load_documents management command."""

from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType


@pytest.fixture
def mock_usecase():
    """Create a mock usecase with default return values."""
    mock = Mock()
    mock.execute.return_value = {"created": 5, "updated": 2, "errors": []}
    return mock


@pytest.fixture
def mock_container_factory(mock_usecase):
    """Create a mock container factory that returns the mock container."""
    mock_container = Mock()
    mock_container.load_documents_usecase.return_value = mock_usecase

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.load_documents.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


@pytest.fixture
def mock_logger():
    """Create a mock logger."""
    with patch(
        "infrastructure.django_apps.ingestion.management.commands.load_documents.logging.getLogger"
    ) as mock_get_logger:
        mock_logger_instance = Mock()
        mock_get_logger.return_value = mock_logger_instance
        yield mock_logger_instance


class TestLoadDocumentsCommand:
    """Test cases for load_documents management command."""

    def test_command_requires_type_argument(self):
        """Test that command fails without --type argument."""
        with pytest.raises(CommandError):
            call_command("load_documents")

    def test_command_rejects_invalid_type(self):
        """Test that command fails with invalid document type."""
        with pytest.raises(CommandError):
            call_command("load_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type",
        [
            DocumentType.OFFERS.value,
            DocumentType.CORPS.value,
        ],
    )
    def test_command_calls_usecase_with_correct_parameters(
        self,
        mock_container_factory,
        mock_usecase,
        mock_logger,
        document_type,
    ):
        """Test that command calls usecase with correct parameters."""
        call_command("load_documents", "--type", document_type)

        mock_container_factory.assert_called_once()
        mock_usecase.execute.assert_called_once()
        call_args = mock_usecase.execute.call_args[0][0]

        assert call_args.operation_type == LoadOperationType.FETCH_FROM_API
        assert call_args.kwargs["document_type"] == DocumentType(document_type)

        mock_logger.info.assert_any_call(f"Loading documents of type: {document_type}")
        mock_logger.info.assert_any_call("✅ Load completed: 5 created, 2 updated")

    def test_command_displays_warnings_for_errors(
        self, mock_container_factory, mock_usecase, mock_logger
    ):
        """Test that command displays warnings when errors occur."""
        mock_usecase.execute.return_value = {
            "created": 3,
            "updated": 1,
            "errors": ["Error 1", "Error 2"],
        }

        call_command("load_documents", "--type", DocumentType.OFFERS.value)

        mock_logger.warning.assert_called_once_with("⚠️  2 errors occurred")

    def test_command_raises_command_error_on_exception(
        self, mock_container_factory, mock_usecase
    ):
        """Test that command raises CommandError when usecase fails."""
        mock_usecase.execute.side_effect = Exception("Database connection failed")

        with pytest.raises(
            CommandError, match="Failed to load documents: Database connection failed"
        ):
            call_command("load_documents", "--type", DocumentType.CORPS.value)

    def test_command_handles_zero_results(
        self, mock_container_factory, mock_usecase, mock_logger
    ):
        """Test command output when no documents are processed."""
        mock_usecase.execute.return_value = {"created": 0, "updated": 0, "errors": []}

        call_command("load_documents", "--type", DocumentType.OFFERS.value)

        mock_logger.info.assert_any_call("✅ Load completed: 0 created, 0 updated")
