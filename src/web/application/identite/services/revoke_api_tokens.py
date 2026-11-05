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


def revoke_api_tokens(*, compte: UserModel, utilisateur: UserModel) -> int:
    with transaction.atomic():
        revoked = compte.revoke_refresh_tokens()
        AuditLogWriter(repository=PostgresAuditLogRepository()).log_action(
            utilisateur_id=utilisateur.username,
            entity=Entity(entity_id=compte.username),
            ressource_kind="Utilisateur",
            event_name="JetonsApiRevoques",
        )
    logger.warning(
        "Revoked %d refresh token(s) of user %s, by user %s.",
        revoked,
        compte.pk,
        utilisateur.pk,
    )
    return revoked
