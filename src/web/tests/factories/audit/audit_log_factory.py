from datetime import datetime, timezone
from uuid import UUID, uuid4

from domain.audit.entities.audit_log import AuditLog
from infrastructure.django_apps.audit.models import AuditLogModel


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

    @staticmethod
    def create_model(
        utilisateur_id: UUID | None = None,
        event_name: str = "ProfilAgentCree",
        ressource_kind: str = "Agent",
        ressource_id: UUID | None = None,
        occurred_at: datetime | None = None,
        event_id: UUID | None = None,
    ) -> AuditLogModel:
        entity = AuditLogFactory.create_entity(
            utilisateur_id=utilisateur_id,
            event_name=event_name,
            ressource_kind=ressource_kind,
            ressource_id=ressource_id,
            occurred_at=occurred_at,
            event_id=event_id,
        )
        model = AuditLogModel.from_entity(entity)
        model.save()
        return model

    @staticmethod
    def create_model_batch(size: int, **kwargs) -> list[AuditLogModel]:
        return [AuditLogFactory.create_model(**kwargs) for _ in range(size)]
