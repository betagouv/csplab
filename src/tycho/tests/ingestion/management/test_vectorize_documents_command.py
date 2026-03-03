from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from domain.entities.document import DocumentType

VECTORIZE_LIMIT = 5


@pytest.fixture
def mock_usecase():
    mock = Mock()
    mock.execute.return_value = {
        "processed": 10,
        "vectorized": 8,
        "errors": 0,
        "error_details": [],
    }
    return mock


@pytest.fixture
def mock_logger():
    return Mock()


@pytest.fixture
def mock_container_factory(mock_usecase, mock_logger):
    mock_container = Mock()
    mock_container.vectorize_documents_usecase.return_value = mock_usecase
    mock_container.logger_service.return_value = mock_logger

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.vectorize_documents.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


class TestVectorizeDocumentsCommand:
    def test_command_requires_type_argument(self):
        with pytest.raises(CommandError):
            call_command("vectorize_documents")

    def test_command_rejects_invalid_type(self):
        with pytest.raises(CommandError):
            call_command("vectorize_documents", "--type", "INVALID_TYPE")

    @pytest.mark.parametrize(
        "document_type,limit,expected_limit",
        [
            (DocumentType.CONCOURS, None, 250),
            (DocumentType.OFFERS, VECTORIZE_LIMIT, VECTORIZE_LIMIT),
        ],
    )
    def test_command_executes_with_correct_parameters(
        self,
        mock_container_factory,
        mock_usecase,
        document_type,
        limit,
        expected_limit,
    ):
        args = ["vectorize_documents", "--type", document_type.value]
        if limit is not None:
            args.extend(["--limit", limit])

        call_command(*args)

        mock_container_factory.assert_called_once()
        mock_usecase.execute.assert_called_once_with(document_type, expected_limit)

    def test_command_logs_output(
        self,
        mock_container_factory,
        mock_usecase,
        mock_logger,
    ):
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

        # Verify logger was called with correct messages
        mock_logger.info.assert_any_call(
            "✅ Vectorization completed: %d of %d vectorized", 3, 5
        )
        mock_logger.warning.assert_any_call("⚠️ %d errors occurred", 2)
        mock_logger.warning.assert_any_call(
            "%s - %s: %s", "OFFERS", "123", "Vectorization failed"
        )
        mock_logger.warning.assert_any_call(
            "%s - %s: %s", "OFFERS", "456", "Invalid data format"
        )

    def test_command_raises_command_error_on_exception(
        self,
        mock_container_factory,
        mock_usecase,
    ):
        mock_usecase.execute.side_effect = Exception("Database connection failed")

        with pytest.raises(
            CommandError,
            match="Failed to vectorize documents: Database connection failed",
        ):
            call_command("vectorize_documents", "--type", DocumentType.CORPS.value)
