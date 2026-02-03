"""Tests for clean_documents management command."""

from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from domain.entities.document import DocumentType


@pytest.fixture
def mock_usecase():
    """Create a mock usecase with default return values."""
    mock = Mock()
    mock.execute.return_value = {
        "cleaned": 3,
        "processed": 5,
        "errors": 0,
        "error_details": [],
    }
    return mock


@pytest.fixture
def mock_container_factory(mock_usecase):
    """Create a mock container factory that returns the mock container."""
    mock_container = Mock()
    mock_container.clean_documents_usecase.return_value = mock_usecase

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.clean_documents.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


class TestCleanDocumentsCommand:
    """Test cases for clean_documents management command."""

    def test_command_requires_type_argument(self):
        """Test that command fails without --type argument."""
        with pytest.raises(CommandError):
            call_command("clean_documents")

    def test_command_rejects_invalid_type(self):
        """Test that command fails with invalid document type."""
        with pytest.raises(CommandError):
            call_command("clean_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type",
        [
            DocumentType.OFFERS.value,
            DocumentType.CORPS.value,
            DocumentType.CONCOURS.value,
        ],
    )
    def test_command_calls_usecase_with_correct_parameters(
        self, mock_container_factory, mock_usecase, document_type, capsys
    ):
        """Test that command calls usecase with correct parameters."""
        call_command("clean_documents", "--type", document_type)

        mock_container_factory.assert_called_once()
        mock_usecase.execute.assert_called_once_with(DocumentType(document_type))

        captured = capsys.readouterr()
        assert f"Cleaning documents of type: {document_type}" in captured.out
        assert "✅ Clean completed: 3/5 documents cleaned" in captured.out

    def test_command_displays_error_details(
        self, mock_container_factory, mock_usecase, capsys
    ):
        """Test that command displays error details when available."""
        mock_usecase.execute.return_value = {
            "cleaned": 1,
            "processed": 3,
            "errors": 2,
            "error_details": [
                {"entity_id": "123", "error": "Validation failed"},
                {"entity_id": "456", "error": "Missing required field"},
            ],
        }

        call_command("clean_documents", "--type", DocumentType.CORPS.value)

        captured = capsys.readouterr()
        assert "✅ Clean completed: 1/3 documents cleaned" in captured.out
        assert "⚠️  2 errors occurred" in captured.out
        assert "Error details:" in captured.out
        assert "Entity 123: Validation failed" in captured.out
        assert "Entity 456: Missing required field" in captured.out

    def test_command_raises_command_error_on_exception(
        self, mock_container_factory, mock_usecase
    ):
        """Test that command raises CommandError when usecase fails."""
        mock_usecase.execute.side_effect = Exception("Database connection failed")

        with pytest.raises(
            CommandError, match="Failed to clean documents: Database connection failed"
        ):
            call_command("clean_documents", "--type", DocumentType.CORPS.value)
