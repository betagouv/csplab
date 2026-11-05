from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from huey.api import PeriodicTask
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.exceptions.exceptions import TaskError
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from presentation.identite.tasks import (
    flush_expired_tokens,
    flush_expired_tokens_periodic,
)


def test_periodic_task_runs_daily_at_0445():
    assert issubclass(flush_expired_tokens_periodic.task_class, PeriodicTask)

    matching = [
        (hour, minute)
        for hour in range(24)
        for minute in range(60)
        if flush_expired_tokens_periodic.task_class().validate_datetime(
            datetime(2026, 6, 1, hour, minute)
        )
    ]

    assert matching == [(4, 45)]


class TestFlushExpiredTokensTask:
    def test_deletes_only_expired_tokens(self, db):
        user = UtilisateurDjangoFactory()
        OutstandingToken.objects.create(
            user=user,
            jti="expired",
            token="",
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        active = RefreshToken.for_user(user)

        flush_expired_tokens.call_local()

        assert list(OutstandingToken.objects.values_list("jti", flat=True)) == [
            active["jti"]
        ]

    def test_raises_task_error_on_failure(self, db):
        with patch(
            "presentation.identite.tasks.call_command",
            side_effect=RuntimeError("boom"),
        ):
            with pytest.raises(TaskError):
                flush_expired_tokens.call_local()
