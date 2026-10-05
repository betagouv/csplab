import logging

from config.logger_names import LoggerName
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.commons.models import AuditLoginLogModel
from infrastructure.django_apps.users.models import UserModel
from infrastructure.django_apps.utils.ip import IPAddressInput

logger = logging.getLogger(LoggerName.IDENTITE)


def _find_user(email: str) -> UserModel | None:
    return UserModel.objects.filter(email__iexact=email).first()


def _describe_account(user: UserModel | None) -> str:
    # Never log the typed email: it identifies a person.
    return f"user {user.pk}" if user else "an unknown account"


def log_login_succeeded(
    *, canal: Canal, user: UserModel, ip_address: IPAddressInput | None
) -> None:
    logger.info("%s login succeeded for user %s.", canal.name, user.pk)
    AuditLoginLogModel.objects.record_attempt(
        canal=canal,
        resultat=Resultat.SUCCES,
        utilisateur_id=user.username,
        ip_address=ip_address,
    )


def log_login_failed(
    *, canal: Canal, email: str, ip_address: IPAddressInput | None
) -> None:
    user = _find_user(email) if email else None
    logger.warning("%s login failed for %s.", canal.name, _describe_account(user))
    AuditLoginLogModel.objects.record_attempt(
        canal=canal,
        resultat=Resultat.ECHEC,
        utilisateur_id=user.username if user else None,
        ip_address=ip_address,
    )
