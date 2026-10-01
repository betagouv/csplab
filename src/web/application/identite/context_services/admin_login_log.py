import logging

from config.logger_names import LoggerName
from infrastructure.django_apps.users.models import UserModel

logger = logging.getLogger(LoggerName.IDENTITE)


def log_admin_login_succeeded(user: UserModel) -> None:
    logger.info("Admin login succeeded for user %s.", user.pk)


def log_admin_login_failed(username: str) -> None:
    user = UserModel.objects.filter(email__iexact=username).first()
    logger.warning(
        "Admin login failed for %s.",
        f"user {user.pk}" if user else "an unknown account",
    )
