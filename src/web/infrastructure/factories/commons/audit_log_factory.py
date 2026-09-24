from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.commons.entities.audit_log import AuditLog


class AuditLogFactory:
    @staticmethod
    def create_entity(
        utilisateur_id: UUID | None = None,
        event_name: str = "ProfilAgentCree",
        ressource_kind: str = "Agent",
        ressource_id: UUID | None = None,
        occurred_at: datetime | None = None,
        event_id: UUID | None = None,
    ) -> AuditLog:
        return AuditLog(
            entity_id=uuid4(),
            event_id=event_id or uuid4(),
            occurred_at=occurred_at or datetime.now(tz=timezone.utc),
            utilisateur_id=utilisateur_id or uuid4(),
            event_name=event_name,
            ressource_kind=ressource_kind,
            ressource_id=ressource_id or uuid4(),
        )
