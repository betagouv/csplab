import logging

from ddd.entity import Entity
from django.db import transaction

from config.logger_names import LoggerName
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.django_apps.users.models import UserModel
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

logger = logging.getLogger(LoggerName.IDENTITE)


def revoke_api_tokens(
    *, account: UserModel, actor: UserModel, deactivate: bool = False
) -> int:
    with transaction.atomic():
        if deactivate:
            account.is_active = False
            account.save(update_fields=["is_active"])
        revoked = account.revoke_refresh_tokens()
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=actor.username,
            entity=Entity(entity_id=account.username),
            ressource_kind="Utilisateur",
            event_name="CompteApiDesactive" if deactivate else "JetonsApiRevoques",
        )
    logger.warning(
        "Revoked %d refresh token(s) of user %s (deactivated: %s), by user %s.",
        revoked,
        account.pk,
        deactivate,
        actor.pk,
    )
    return revoked
