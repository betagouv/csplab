import logging

from django.contrib.sessions.backends.db import SessionStore
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
        SessionStore.clear_expired()
    except Exception as e:
        raise TaskError(
            message="Failed to clear expired sessions",
            details={"error": str(e)},
        ) from e
    logger.info("Cleared expired sessions.")
