from datetime import datetime, timezone
from uuid import UUID

from ddd.aggregate_root import AggregateRoot
from ddd.domain_event import DomainEvent
from ddd.entity import Entity

from domain.commons.entities.audit_log import AuditLog
from domain.commons.repositories.audit_log_repository_interface import (
    IAuditLogRepository,
)


class AuditLogWriter:
    def __init__(self, repository: IAuditLogRepository) -> None:
        self._repository = repository

    def drain_events(self, *, utilisateur_id: UUID, aggregate: AggregateRoot) -> None:
        for event in aggregate.collect_events():
            self._log_event(utilisateur_id=utilisateur_id, event=event)

    def log_action(
        self,
        *,
        utilisateur_id: UUID,
        entity: Entity,
        ressource_kind: str,
        event_name: str,
    ) -> None:
        self._repository.store_log(
            AuditLog(
                event_id=None,
                occurred_at=datetime.now(tz=timezone.utc),
                utilisateur_id=utilisateur_id,
                ressource_kind=ressource_kind,
                ressource_id=entity.entity_id,
                event_name=event_name,
            )
        )

    def _log_event(self, *, utilisateur_id: UUID, event: DomainEvent) -> None:
        if event.metadata is None:
            return

        self._repository.store_log(
            AuditLog(
                event_id=event.event_id,
                occurred_at=event.occurred_at,
                utilisateur_id=utilisateur_id,
                ressource_kind=event.metadata.aggregate,
                ressource_id=event.metadata.aggregate_id,
                event_name=event.metadata.event_name,
            )
        )
