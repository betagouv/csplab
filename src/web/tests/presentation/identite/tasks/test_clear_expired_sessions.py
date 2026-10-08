from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from django.contrib.sessions.models import Session
from django.utils import timezone
from huey.api import PeriodicTask

from infrastructure.exceptions.exceptions import TaskError
from presentation.identite.tasks import (
    clear_expired_sessions,
    clear_expired_sessions_periodic,
)


def test_periodic_task_runs_daily_at_0430():
    assert issubclass(clear_expired_sessions_periodic.task_class, PeriodicTask)

    matching = [
        (hour, minute)
        for hour in range(24)
        for minute in range(60)
        if clear_expired_sessions_periodic.task_class().validate_datetime(
            datetime(2026, 6, 1, hour, minute)
        )
    ]

    assert matching == [(4, 30)]


class TestClearExpiredSessionsTask:
    def test_deletes_expired_sessions(self, db):
        Session.objects.create(
            session_key="expired",
            session_data="",
            expire_date=timezone.now() - timedelta(minutes=1),
        )

        clear_expired_sessions.call_local()

        assert Session.objects.count() == 0

    def test_keeps_active_sessions(self, db):
        Session.objects.create(
            session_key="active",
            session_data="",
            expire_date=timezone.now() + timedelta(days=1),
        )

        clear_expired_sessions.call_local()

        assert Session.objects.filter(session_key="active").exists()

    def test_raises_task_error_on_failure(self, db):
        with patch(
            "django.contrib.sessions.backends.db.SessionStore.clear_expired",
            side_effect=RuntimeError("boom"),
        ):
            with pytest.raises(TaskError):
                clear_expired_sessions.call_local()

    def test_follows_configured_session_engine(self, settings):
        settings.SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

        with patch(
            "django.contrib.sessions.backends.cached_db.SessionStore.clear_expired"
        ) as clear_expired:
            clear_expired_sessions.call_local()

        clear_expired.assert_called_once_with()
