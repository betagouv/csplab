import logging
from importlib import import_module

from django.conf import settings
from django.core.management import call_command
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, lock_task

from config.logger_names import LoggerName
from infrastructure.exceptions.exceptions import TaskError


@db_periodic_task(crontab(hour="4", minute="30"))
@lock_task("clear-expired-sessions-periodic")
def clear_expired_sessions_periodic():
    clear_expired_sessions()


@db_task()
def clear_expired_sessions():
    logger = logging.getLogger(LoggerName.IDENTITE.value)

    try:
        engine = import_module(settings.SESSION_ENGINE)
        engine.SessionStore.clear_expired()
    except Exception as e:
        raise TaskError(
            message="Failed to clear expired sessions",
            details={"error": str(e)},
        ) from e
    logger.info("Cleared expired sessions.")


@db_periodic_task(crontab(hour="4", minute="45"))
@lock_task("flush-expired-tokens-periodic")
def flush_expired_tokens_periodic():
    flush_expired_tokens()


@db_task()
def flush_expired_tokens():
    logger = logging.getLogger(LoggerName.IDENTITE.value)

    try:
        call_command("flushexpiredtokens")
    except Exception as e:
        raise TaskError(
            message="Failed to flush expired JWT tokens",
            details={"error": str(e)},
        ) from e
    logger.info("Flushed expired JWT tokens.")
