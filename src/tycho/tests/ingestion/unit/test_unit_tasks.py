from unittest.mock import MagicMock, call, patch

import pytest
from huey.api import PeriodicTask

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.entities.document import DocumentType
from infrastructure.django_apps.ingestion.tasks import (
    clean_concours,
    clean_corps,
    clean_documents,
    clean_offers,
    load_corps,
    load_documents,
    load_offers,
    vectorize_concours,
    vectorize_corps,
    vectorize_documents,
    vectorize_offers,
)
from infrastructure.exceptions.exceptions import TaskError


@pytest.fixture
def mock_container():
    with patch(
        "infrastructure.django_apps.ingestion.tasks.create_ingestion_container"
    ) as mock_factory:
        mock_container = MagicMock()
        mock_factory.return_value = mock_container
        yield mock_container


class TestLoadDocumentsTasks:
    @pytest.mark.parametrize(
        "task, kwargs",
        [
            (load_corps, {"document_type": DocumentType.CORPS}),
            (
                load_offers,
                {
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 100,
                },
            ),
        ],
    )
    def test_periodic_task_does_not_call_usecase(self, mock_container, task, kwargs):
        assert issubclass(task.task_class, PeriodicTask)
        task.call_local()
        mock_container.load_documents_usecase.assert_not_called()

    @pytest.mark.parametrize(
        "kwargs, created, updated",
        [
            ({"document_type": DocumentType.CORPS}, 3, 2),
            (
                {
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 100,
                },
                30,
                20,
            ),
        ],
    )
    def test_calls_usecase_and_logs(self, mock_container, kwargs, created, updated):
        usecase = MagicMock()
        usecase.execute.return_value = {
            "created": created,
            "updated": updated,
            "errors": ["failed", "failed"],
        }
        mock_container.load_documents_usecase.return_value = usecase

        load_documents.call_local(kwargs)

        mock_container.load_documents_usecase.assert_called_once()
        usecase.execute.assert_called_once_with(
            LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs=kwargs,
            )
        )
        logger = mock_container.logger_service.return_value
        logger.info.assert_called_once_with(
            "✅ Load completed: %d created, %d updated", created, updated
        )
        logger.warning.assert_called_once_with("⚠️ %d errors occurred", 2)

    @pytest.mark.parametrize(
        "kwargs, expected_message",
        [
            (
                {"document_type": DocumentType.CORPS},
                "Failed to load documents type CORPS",
            ),
            (
                {
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 100,
                },
                "Failed to load documents type OFFERS",
            ),
        ],
    )
    def test_raises_task_error_on_failure(
        self, mock_container, kwargs, expected_message
    ):
        usecase = MagicMock()
        usecase.execute.side_effect = Exception("boom")
        mock_container.load_documents_usecase.return_value = usecase

        with pytest.raises(TaskError) as exc_info:
            load_documents.call_local(kwargs)

        assert exc_info.value.message == expected_message


class TestCleanTasks:
    @pytest.mark.parametrize("task", [clean_corps, clean_concours, clean_offers])
    def test_periodic_task_does_not_call_usecase(self, mock_container, task):
        assert issubclass(task.task_class, PeriodicTask)
        task.call_local()
        mock_container.clean_documents_usecase.assert_not_called()

    def test_calls_usecase_and_logs(self, mock_container):
        usecase = MagicMock()
        usecase.execute.return_value = {
            "cleaned": 9,
            "processed": 10,
            "errors": 1,
            "error_details": [{"entity_id": 123, "error": "failed"}],
        }
        mock_container.clean_documents_usecase.return_value = usecase

        clean_documents.call_local(DocumentType.OFFERS)

        mock_container.clean_documents_usecase.assert_called_once()
        usecase.execute.assert_called_once_with(DocumentType.OFFERS)
        logger = mock_container.logger_service.return_value
        logger.info.assert_called_once_with(
            "✅ Clean completed: %d/%d documents of type %s cleaned",
            9,
            10,
            DocumentType.OFFERS,
        )
        logger.warning.assert_has_calls(
            [call("⚠️ %d errors occurred", 1), call("Entity %s: %s", 123, "failed")]
        )

    def test_raises_task_error_on_failure(self, mock_container):
        usecase = MagicMock()
        usecase.execute.side_effect = Exception("boom")
        mock_container.clean_documents_usecase.return_value = usecase

        with pytest.raises(TaskError) as exc_info:
            clean_documents.call_local(DocumentType.OFFERS)

        assert (
            exc_info.value.message == f"Failed to clean documents {DocumentType.OFFERS}"
        )


class TestVectorizeTasks:
    @pytest.mark.parametrize(
        "task", [vectorize_corps, vectorize_concours, vectorize_offers]
    )
    def test_periodic_task_does_not_call_usecase(self, mock_container, task):
        assert issubclass(task.task_class, PeriodicTask)
        task.call_local()
        mock_container.vectorize_documents_usecase.assert_not_called()

    def test_calls_usecase_and_logs(self, mock_container):
        usecase = MagicMock()
        usecase.execute.return_value = {
            "vectorized": 9,
            "processed": 10,
            "errors": 1,
            "error_details": [
                {"source_type": "abc", "source_id": 123, "error": "failed"}
            ],
        }
        mock_container.vectorize_documents_usecase.return_value = usecase

        vectorize_documents.call_local(DocumentType.OFFERS)

        mock_container.vectorize_documents_usecase.assert_called_once()
        usecase.execute.assert_called_once_with(DocumentType.OFFERS)
        logger = mock_container.logger_service.return_value
        logger.info.assert_called_once_with(
            "✅ Vectorization completed: %d/%d documents of type %s vectorized",
            9,
            10,
            DocumentType.OFFERS,
        )
        logger.warning.assert_has_calls(
            [call("⚠️ %d errors occurred", 1), call("%s - %s: %s", "abc", 123, "failed")]
        )

    def test_raises_task_error_on_failure(self, mock_container):
        usecase = MagicMock()
        usecase.execute.side_effect = Exception("boom")
        mock_container.vectorize_documents_usecase.return_value = usecase

        with pytest.raises(TaskError) as exc_info:
            vectorize_documents.call_local(DocumentType.OFFERS)

        assert (
            exc_info.value.message
            == f"Failed to vectorize documents {DocumentType.OFFERS}"
        )
