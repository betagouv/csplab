from datetime import datetime
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.core.management import call_command

METHOD = "presentation.ingestion.management.commands.archive_offers.archive_offers"


@patch(METHOD)
def test_command_calls_usecase_with_default_datetime(mock_task, db):
    call_command("archive_offers")

    mock_task.assert_called_once()
    called_with = mock_task.call_args.kwargs["updated_after"]
    expected = datetime.now() - relativedelta(hours=24)
    assert abs((called_with - expected).total_seconds()) < 5  # noqa


@patch(METHOD)
def test_command_calls_usecase_with_arg(mock_task, db):
    updated_after = "2026-01-01T00:00:00"
    call_command("archive_offers", updated_after=updated_after)

    mock_task.assert_called_once_with(updated_after=updated_after)
