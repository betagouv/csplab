import logging

from config.logger_names import LoggerName
from infrastructure.django_apps.users.models import UserModel

logger = logging.getLogger(LoggerName.IDENTITE)


def _describe_account(email: str) -> str:
    # Never log the typed email: it identifies a person.
    user = UserModel.objects.filter(email__iexact=email).first()
    return f"user {user.pk}" if user else "an unknown account"


def log_admin_login_succeeded(user: UserModel) -> None:
    logger.info("Admin login succeeded for user %s.", user.pk)


def log_admin_login_failed(username: str) -> None:
    logger.warning("Admin login failed for %s.", _describe_account(username))


def log_api_login_succeeded(email: str) -> None:
    logger.info("API login succeeded for %s.", _describe_account(email))


def log_api_login_failed(email: str) -> None:
    logger.warning("API login failed for %s.", _describe_account(email))
