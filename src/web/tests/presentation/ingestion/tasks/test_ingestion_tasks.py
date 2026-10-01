from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock, call, patch

import pytest
from huey.api import PeriodicTask
from huey.contrib.djhuey import lock_task
from huey.exceptions import TaskLockedException

from application.ingestion.interfaces.load_documents_input import LoadDocumentsInput
from application.ingestion.interfaces.load_operation_type import LoadOperationType
from domain.ingestion.entities.document import DocumentType
from infrastructure.exceptions.exceptions import TaskError
from presentation.ingestion.tasks import (
    clean_documents,
    ingest_concours,
    ingest_corps,
    ingest_metiers,
    load_documents,
    vectorize_documents,
    vectorize_offers,
)


@pytest.mark.parametrize(
    "task",
    [ingest_corps, ingest_metiers, ingest_concours],
)
def test_periodic_task_runs_once_per_scheduled_hour(task):
    first_day_of_month = datetime(2026, 6, 1)
    matching_minutes = [
        minute
        for hour in range(24)
        for minute in range(60)
        if task.task_class().validate_datetime(
            first_day_of_month.replace(hour=hour, minute=minute)
        )
    ]

    assert len(matching_minutes) == 1


def _pipeline_steps(task):
    steps = []
    while task is not None:
        steps.append((type(task), task.args, task.kwargs))
        task = task.on_complete
    return steps


class TestIngestionPipelines:
    @pytest.fixture
    def mock_huey(self):
        with patch("presentation.ingestion.tasks.HUEY") as mock:
            yield mock

    @pytest.mark.parametrize(
        ("task", "document_type"),
        [
            pytest.param(ingest_corps, DocumentType.CORPS, id="corps"),
            pytest.param(ingest_metiers, DocumentType.METIERS, id="metiers"),
        ],
    )
    def test_loads_then_cleans_then_vectorizes(
        self, mock_huey, mock_container, task, document_type
    ):
        assert issubclass(task.task_class, PeriodicTask)

        task.call_local()

        mock_huey.enqueue.assert_called_once()
        (pipeline,) = mock_huey.enqueue.call_args.args
        assert _pipeline_steps(pipeline) == [
            (
                load_documents.task_class,
                ({"document_type": document_type},),
                {"usecase_name": "load_documents_usecase"},
            ),
            (clean_documents.task_class, (document_type,), {}),
            (vectorize_documents.task_class, (document_type,), {}),
        ]
        mock_container.load_documents_usecase.assert_not_called()

    def test_concours_cleans_then_vectorizes(self, mock_huey, mock_container):
        assert issubclass(ingest_concours.task_class, PeriodicTask)

        ingest_concours.call_local()

        mock_huey.enqueue.assert_called_once()
        (pipeline,) = mock_huey.enqueue.call_args.args
        assert _pipeline_steps(pipeline) == [
            (clean_documents.task_class, (DocumentType.CONCOURS,), {}),
            (vectorize_documents.task_class, (DocumentType.CONCOURS,), {}),
        ]
        mock_container.clean_documents_usecase.assert_not_called()


@pytest.fixture
def mock_container():
    with patch(
        "presentation.ingestion.tasks.create_ingestion_container"
    ) as mock_factory:
        mock_container = MagicMock()
        mock_factory.return_value = mock_container
        yield mock_container


class TestLoadDocumentsTasks:
    CASES = [
        pytest.param(
            {
                "kwargs": {"document_type": DocumentType.CORPS},
                "usecase_name": "load_documents_usecase",
            },
            id="corps",
        ),
        pytest.param(
            {
                "kwargs": {"document_type": DocumentType.METIERS},
                "usecase_name": "load_documents_usecase",
            },
            id="metiers",
        ),
    ]

    @pytest.fixture(params=CASES)
    def case(self, request):
        return request.param

    @pytest.fixture
    def usecase(self, mock_container, case):
        mock = AsyncMock()
        getattr(mock_container, case["usecase_name"]).return_value = mock
        return mock

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

    def test_does_not_run_concurrently_for_same_document_type(self, mock_container):
        with lock_task(f"clean-documents-{DocumentType.CORPS.value}"):
            with pytest.raises(TaskLockedException):
                clean_documents.call_local(DocumentType.CORPS)

        mock_container.clean_documents_usecase.assert_not_called()

    def test_runs_concurrently_for_other_document_type(self, mock_container):
        usecase = MagicMock()
        usecase.execute.return_value = {"cleaned": 0, "processed": 0, "errors": 0}
        mock_container.clean_documents_usecase.return_value = usecase

        with lock_task(f"clean-documents-{DocumentType.CORPS.value}"):
            clean_documents.call_local(DocumentType.METIERS)

        usecase.execute.assert_called_once_with(DocumentType.METIERS)


class TestVectorizeTasks:
    def test_periodic_task_does_not_call_usecase(self, mock_container):
        assert issubclass(vectorize_offers.task_class, PeriodicTask)
        vectorize_offers.call_local()
        mock_container.vectorize_documents_usecase.assert_not_called()

    def test_calls_usecase_and_logs(self, mock_container):
        usecase = Mock()
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
