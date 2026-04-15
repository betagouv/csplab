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
    CASES = [
        pytest.param(
            {
                "task": load_corps,
                "kwargs": {"document_type": DocumentType.CORPS},
                "usecase_name": "load_documents_usecase",
            },
            id="corps",
        ),
        pytest.param(
            {
                "task": load_offers,
                "kwargs": {
                    "document_type": DocumentType.OFFERS,
                    "reload": False,
                    "batch_size": 100,
                },
                "usecase_name": "load_offers_usecase",
            },
            id="offers",
        ),
    ]

    @pytest.fixture(params=CASES)
    def case(self, request):
        return request.param

    @pytest.fixture
    def usecase(self, mock_container, case):
        mock = MagicMock()
        getattr(mock_container, case["usecase_name"]).return_value = mock
        return mock

    def test_is_periodic_task(self, case):
        assert issubclass(case["task"].task_class, PeriodicTask)

    def test_periodic_task_does_not_call_usecase(self, mock_container, case):
        case["task"].call_local()
        getattr(mock_container, case["usecase_name"]).assert_not_called()

    def test_calls_correct_usecase(self, mock_container, usecase, case):
        usecase.execute.return_value = {"created": 3, "updated": 2, "errors": []}

        load_documents.call_local(case["kwargs"], case["usecase_name"])

        getattr(mock_container, case["usecase_name"]).assert_called_once()
        usecase.execute.assert_called_once_with(
            LoadDocumentsInput(
                operation_type=LoadOperationType.FETCH_FROM_API,
                kwargs=case["kwargs"],
            )
        )

    def test_logs_results(self, mock_container, usecase, case):
        created, updated = 3, 2
        usecase.execute.return_value = {
            "created": created,
            "updated": updated,
            "errors": ["failed", "failed"],
        }

        load_documents.call_local(case["kwargs"], case["usecase_name"])

        logger = mock_container.logger_service.return_value
        logger.info.assert_called_once_with(
            "✅ Load completed: %d created, %d updated", created, updated
        )
        logger.warning.assert_called_once_with("⚠️ %d errors occurred", 2)

    def test_raises_task_error_on_failure(self, usecase, case):
        usecase.execute.side_effect = Exception("boom")

        with pytest.raises(TaskError) as exc_info:
            load_documents.call_local(case["kwargs"], case["usecase_name"])

        document_type = case["kwargs"]["document_type"]
        assert (
            exc_info.value.message
            == f"Failed to load documents type {document_type.value}"
        )


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
