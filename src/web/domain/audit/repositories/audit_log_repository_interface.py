from typing import Protocol
from uuid import UUID

from domain.audit.entities.audit_log import AuditLog


class IAuditLogRepository(Protocol):
    def store_log(self, audit_log: AuditLog) -> None: ...
    def get_logs_for_ressource(
        self, ressource_kind: str, ressource_id: UUID
    ) -> list[AuditLog]: ...
