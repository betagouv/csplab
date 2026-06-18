from uuid import UUID

from domain.commons.entities.audit_log import AuditLog
from domain.commons.repositories.audit_log_repository_interface import (
    IAuditLogRepository,
)
from infrastructure.django_apps.commons.models import AuditLogModel


class PostgresAuditLogRepository(IAuditLogRepository):
    def store_log(self, audit_log: AuditLog) -> None:
        AuditLogModel.from_entity(audit_log).save()

    def get_logs_for_ressource(
        self, ressource_kind: str, ressource_id: UUID
    ) -> list[AuditLog]:
        return [
            model.to_entity()
            for model in AuditLogModel.objects.filter(
                ressource_kind=ressource_kind,
                ressource_id=ressource_id,
            )
        ]
