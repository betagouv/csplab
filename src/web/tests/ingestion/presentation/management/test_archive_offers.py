from datetime import datetime
from unittest.mock import patch

import pytest
from dateutil.relativedelta import relativedelta
from django.core.management import call_command

METHOD = "presentation.ingestion.management.commands.archive_offers.archive_offers"


@pytest.mark.django_db
def test_command_calls_usecase_with_default_datetime():
    with patch(METHOD) as mock_task:
        call_command("archive_offers")
        mock_task.assert_called_once()
        called_with = mock_task.call_args.kwargs["updated_after"]
        expected = datetime.now() - relativedelta(hours=24)
        assert abs((called_with - expected).total_seconds()) < 5  # noqa


@pytest.mark.django_db
def test_command_calls_usecase_with_arg():
    updated_after = "2026-01-01T00:00:00"
    with patch(METHOD) as mock_task:
        call_command("archive_offers", updated_after=updated_after)
        mock_task.assert_called_once_with(updated_after=updated_after)
