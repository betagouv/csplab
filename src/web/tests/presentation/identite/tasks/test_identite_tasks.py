from unittest.mock import MagicMock, patch

import pytest
from huey.api import PeriodicTask

from infrastructure.exceptions.exceptions import TaskError
from presentation.identite.tasks import (
    import_etablissements_finess,
    import_etablissements_finess_periodic,
)


@pytest.fixture
def mock_container():
    with patch("presentation.identite.tasks.create_identite_container") as mock_factory:
        mock_container = MagicMock()
        mock_factory.return_value = mock_container
        yield mock_container


def test_is_periodic_task():
    assert issubclass(import_etablissements_finess_periodic.task_class, PeriodicTask)


def test_periodic_task_does_not_call_usecase(mock_container):
    import_etablissements_finess_periodic.call_local()

    mock_container.import_etablissements_finess_usecase.assert_not_called()


def test_calls_usecase_and_logs(mock_container):
    usecase = MagicMock()
    usecase.execute.return_value = {"created": 3, "updated": 2, "errors": []}
    mock_container.import_etablissements_finess_usecase.return_value = usecase

    import_etablissements_finess.call_local()

    mock_container.import_etablissements_finess_usecase.assert_called_once()
    usecase.execute.assert_called_once()
    logger = mock_container.logger_service.return_value
    logger.info.assert_called_once_with(
        "✅ Import FINESS terminé : %d créés, %d mis à jour", 3, 2
    )
    logger.warning.assert_not_called()


def test_logs_warning_on_errors(mock_container):
    usecase = MagicMock()
    usecase.execute.return_value = {
        "created": 1,
        "updated": 0,
        "errors": [{"entity_id": "010780195", "error": "SIRET invalide"}],
    }
    mock_container.import_etablissements_finess_usecase.return_value = usecase

    import_etablissements_finess.call_local()

    logger = mock_container.logger_service.return_value
    logger.warning.assert_any_call("⚠️ %d erreurs rencontrées", 1)
    logger.warning.assert_any_call(
        "Etablissement %s: %s", "010780195", "SIRET invalide"
    )


def test_raises_task_error_on_failure(mock_container):
    usecase = MagicMock()
    usecase.execute.side_effect = Exception("boom")
    mock_container.import_etablissements_finess_usecase.return_value = usecase

    with pytest.raises(TaskError) as exc_info:
        import_etablissements_finess.call_local()

    assert exc_info.value.message == "Failed to import etablissements FINESS"
