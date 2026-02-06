"""Tests for vectorize_documents management command."""

from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from domain.entities.document import DocumentType

VECTORIZE_LIMIT = 5


@pytest.fixture
def mock_usecase():
    """Create a mock usecase with default return values."""
    mock = Mock()
    mock.execute.return_value = {
        "processed": 10,
        "vectorized": 8,
        "errors": 0,
        "error_details": [],
    }
    return mock


@pytest.fixture
def mock_repository():
    """Create a mock repository with default return values."""
    mock = Mock()
    mock.get_all.return_value = [Mock() for _ in range(10)]
    return mock


@pytest.fixture
def mock_repository_factory(mock_repository):
    """Create a mock repository factory."""
    mock = Mock()
    mock.get_repository.return_value = mock_repository
    return mock


@pytest.fixture
def mock_container_factory(mock_usecase, mock_repository_factory):
    """Create a mock container factory that returns the mock container."""
    mock_container = Mock()
    mock_container.vectorize_documents_usecase.return_value = mock_usecase
    mock_container.repository_factory.return_value = mock_repository_factory

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.vectorize_documents.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


class TestVectorizeDocumentsCommand:
    """Test cases for vectorize_documents management command."""

    def test_command_requires_type_argument(self):
        """Test that command fails without --type argument."""
        with pytest.raises(CommandError):
            call_command("vectorize_documents")

    def test_command_rejects_invalid_type(self):
        """Test that command fails with invalid document type."""
        with pytest.raises(CommandError):
            call_command("vectorize_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type",
        [
            DocumentType.CORPS.value,
            DocumentType.CONCOURS.value,
            DocumentType.OFFERS.value,
        ],
    )
    def test_command_accepts_valid_document_types(
        self,
        mock_container_factory,
        mock_usecase,
        mock_repository_factory,
        document_type,
    ):
        """Test that command accepts all valid document types including OFFERS."""
        call_command("vectorize_documents", "--type", document_type)

        mock_container_factory.assert_called_once()
        mock_repository_factory.get_repository.assert_called_once_with(
            DocumentType(document_type)
        )
        mock_usecase.execute.assert_called_once()

    def test_command_respects_limit_parameter(
        self,
        mock_container_factory,
        mock_usecase,
        mock_repository,
        capsys,
    ):
        """Test that command respects the --limit parameter."""
        call_command(
            "vectorize_documents",
            "--type",
            DocumentType.OFFERS.value,
            "--limit",
            VECTORIZE_LIMIT,
        )

        mock_repository.get_all.assert_called_once()
        mock_usecase.execute.assert_called_once()

        # Verify only limited entities are passed
        call_args = mock_usecase.execute.call_args[0][0]
        assert len(call_args) == VECTORIZE_LIMIT

        captured = capsys.readouterr()
        assert "Fetching 5 entities of type: OFFERS" in captured.out
        assert "Vectorizing 5 entities..." in captured.out

    def test_command_handles_empty_repository(
        self,
        mock_container_factory,
        mock_repository,
        capsys,
    ):
        """Test that command handles empty repository gracefully."""
        mock_repository.get_all.return_value = []

        call_command("vectorize_documents", "--type", DocumentType.OFFERS.value)

        captured = capsys.readouterr()
        assert "No entities found for type: OFFERS" in captured.out

        captured = capsys.readouterr()

    def test_command_displays_warnings_and_error_details(
        self,
        mock_container_factory,
        mock_usecase,
        capsys,
    ):
        """Test that command displays detailed error information."""
        mock_usecase.execute.return_value = {
            "processed": 5,
            "vectorized": 3,
            "errors": 2,
            "error_details": [
                {
                    "source_type": "OFFERS",
                    "source_id": "123",
                    "error": "Vectorization failed",
                },
                {
                    "source_type": "OFFERS",
                    "source_id": "456",
                    "error": "Invalid data format",
                },
            ],
        }

        call_command("vectorize_documents", "--type", DocumentType.OFFERS.value)

        captured = capsys.readouterr()
        assert "✅ Completed: 3/5 documents vectorized" in captured.out
        assert "⚠️  2 errors occurred" in captured.out
        assert "Error details:" in captured.out
        assert "OFFERS 123:Vectorization failed" in captured.out
        assert "OFFERS 456:Invalid data format" in captured.out

    def test_command_raises_command_error_on_exception(
        self,
        mock_container_factory,
        mock_usecase,
    ):
        """Test that command raises CommandError when usecase fails."""
        mock_usecase.execute.side_effect = Exception("Database connection failed")

        with pytest.raises(
            CommandError,
            match="Failed to vectorize documents: Database connection failed",
        ):
            call_command("vectorize_documents", "--type", DocumentType.CORPS.value)
