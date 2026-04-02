from unittest.mock import Mock, patch

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType


@pytest.fixture
def mock_usecase():
    mock = Mock()
    mock.execute.return_value = {
        "created": 3,
        "updated": 2,
        "errors": [],
    }
    return mock


@pytest.fixture
def mock_container_factory(mock_usecase):
    mock_container = Mock()
    mock_container.load_offers_usecase.return_value = mock_usecase
    mock_container.logger_service.return_value = Mock()

    with patch(
        "infrastructure.django_apps.ingestion.management.commands.load_offers.create_ingestion_container"
    ) as mock_factory:
        mock_factory.return_value = mock_container
        yield mock_factory


class TestLoadOffersCommand:
    def test_command_calls_usecase_with_default_parameters(
        self, mock_container_factory, mock_usecase
    ):
        call_command("load_offers")

        mock_container_factory.assert_called_once()
        logger = mock_container_factory.return_value.logger_service.return_value

        mock_usecase.execute.assert_called_once_with(
            LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 100,
                },
            )
        )

        logger.info.assert_any_call(
            "✅ Load completed: %d created, %d updated",
            3,
            2,
        )

    def test_command_calls_usecase_with_reload_flag(
        self, mock_container_factory, mock_usecase
    ):
        call_command("load_offers", "--reload")

        mock_usecase.execute.assert_called_once_with(
            LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={
                    "document_type": DocumentType.OFFERS,
                    "reload": True,
                    "batch_size": 100,
                },
            )
        )

    def test_command_calls_usecase_with_custom_batch_size(
        self, mock_container_factory, mock_usecase
    ):
        call_command("load_offers", "--batch-size", "50")

        mock_usecase.execute.assert_called_once_with(
            LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs={
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 50,
                },
            )
        )

    def test_command_raises_command_error_on_exception(
        self, mock_container_factory, mock_usecase
    ):
        mock_usecase.execute.side_effect = Exception("API connection failed")

        with pytest.raises(
            CommandError, match="Failed to load documents: API connection failed"
        ):
            call_command("load_offers")
