import logging

from config.logger_names import LoggerName
from infrastructure.django_apps.users.models import UserModel

logger = logging.getLogger(LoggerName.IDENTITE)


def log_api_login_succeeded(email: str) -> None:
    user = UserModel.objects.filter(email__iexact=email).first()
    logger.info("API login succeeded for user %s.", user.pk if user else "unknown")


def log_api_login_failed(email: str) -> None:
    # Never log the typed email: it identifies a person.
    user = UserModel.objects.filter(email__iexact=email).first()
    logger.warning(
        "API login failed for %s.",
        f"user {user.pk}" if user else "an unknown account",
    )
