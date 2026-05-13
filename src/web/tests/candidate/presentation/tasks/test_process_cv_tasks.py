from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

from presentation.candidate.tasks import process_cv_task

CV_UUID = str(uuid4())
CV_BYTES = b"fake pdf content"


def test_process_cv_task_is_enqueued():
    with patch(
        "infrastructure.di.candidate.candidate_factory.create_candidate_container"
    ) as mock_factory:
        process_cv_task(CV_UUID, CV_BYTES)

    mock_factory.assert_not_called()


def test_process_cv_task_calls_usecase(db):
    mock_execute = AsyncMock()
    mock_usecase = MagicMock()
    mock_usecase.execute = mock_execute

    mock_container = MagicMock()
    mock_container.process_uploaded_cv_usecase.return_value = mock_usecase

    with patch(
        "presentation.candidate.tasks.create_candidate_container",
        return_value=mock_container,
    ):
        process_cv_task.call_local(CV_UUID, CV_BYTES)

    mock_container.process_uploaded_cv_usecase.assert_called_once()
    mock_execute.assert_awaited_once_with(UUID(CV_UUID), CV_BYTES)
