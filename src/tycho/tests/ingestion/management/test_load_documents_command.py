from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from application.ingestion.interfaces.load_operation_type import LoadOperationType


@pytest.fixture
def mock_usecase():
    mock = Mock()
    mock.execute.return_value = {"created": 5, "updated": 2, "errors": []}
    return mock


@pytest.fixture
def mock_container_factory(mock_usecase):
    mock_container = Mock()
    mock_container.load_documents_usecase.return_value = mock_usecase

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.load_documents.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


class TestLoadDocumentsCommand:
    def test_command_calls_usecase_with_correct_parameters(
        self,
        mock_container_factory,
        mock_usecase,
    ):
        call_command("load_documents")

        mock_container_factory.assert_called_once()
        mock_usecase.execute.assert_called_once()
        call_args = mock_usecase.execute.call_args[0][0]

        assert call_args.operation_type == LoadOperationType.FETCH_FROM_API

        mock_logger = mock_container_factory.return_value.logger_service.return_value
        mock_logger.info.assert_any_call(
            "✅ Load completed: %d created, %d updated", 5, 2
        )

    def test_command_displays_warnings_for_errors(
        self, mock_container_factory, mock_usecase
    ):
        mock_usecase.execute.return_value = {
            "created": 3,
            "updated": 1,
            "errors": ["Error 1", "Error 2"],
        }

        call_command("load_documents")

        mock_logger = mock_container_factory.return_value.logger_service.return_value
        mock_logger.warning.assert_called_once_with("⚠️ %d errors occurred", 2)

    def test_command_raises_command_error_on_exception(
        self, mock_container_factory, mock_usecase
    ):
        mock_usecase.execute.side_effect = Exception("Database connection failed")

        with pytest.raises(
            CommandError, match="Failed to load documents: Database connection failed"
        ):
            call_command("load_documents")

    def test_command_handles_zero_results(self, mock_container_factory, mock_usecase):
        mock_usecase.execute.return_value = {"created": 0, "updated": 0, "errors": []}

        call_command("load_documents")

        mock_logger = mock_container_factory.return_value.logger_service.return_value
        mock_logger.info.assert_any_call(
            "✅ Load completed: %d created, %d updated", 0, 0
        )
