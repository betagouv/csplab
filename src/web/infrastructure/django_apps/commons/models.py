import uuid

from django.db import models

from domain.commons.entities.audit_log import AuditLog
from domain.commons.entities.stats_history import StatsHistory
from infrastructure.django_apps.utils.models import BaseDatedModel


class StatsHistoryModel(BaseDatedModel):
    date = models.DateField()
    metric_name = models.CharField(max_length=255)
    metric_value = models.BigIntegerField()

    class Meta:
        db_table = "stats_history"
        verbose_name = "Stats History"
        verbose_name_plural = "Stats History"
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["date", "metric_name"],
                name="unique_stats_history_date_metric_name",
            ),
        ]

    def to_entity(self) -> StatsHistory:
        return StatsHistory(
            date=self.date,
            metric_name=self.metric_name,
            metric_value=self.metric_value,
        )

    @classmethod
    def from_entity(cls, stats_history: StatsHistory) -> "StatsHistoryModel":
        return cls(
            id=uuid.uuid4(),
            date=stats_history.date,
            metric_name=stats_history.metric_name,
            metric_value=stats_history.metric_value,
        )


class AuditLogModel(BaseDatedModel):
    event_id = models.UUIDField(db_index=True, null=True)
    occurred_at = models.DateTimeField()
    utilisateur_id = models.UUIDField()
    event_name = models.CharField(max_length=255)
    ressource_kind = models.CharField(max_length=255)
    ressource_id = models.UUIDField()

    class Meta:
        db_table = "audit_logs"
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(
                fields=["ressource_kind", "ressource_id"],
                name="audit_logs_ressource_idx",
            ),
            models.Index(fields=["utilisateur_id"], name="audit_logs_utilisateur_idx"),
        ]

    def to_entity(self) -> AuditLog:
        return AuditLog(
            entity_id=self.id,
            event_id=self.event_id,
            occurred_at=self.occurred_at,
            utilisateur_id=self.utilisateur_id,
            ressource_kind=self.ressource_kind,
            ressource_id=self.ressource_id,
            event_name=self.event_name,
        )

    @classmethod
    def from_entity(cls, audit_log: AuditLog) -> "AuditLogModel":
        return cls(
            id=audit_log.entity_id,
            event_id=audit_log.event_id,
            occurred_at=audit_log.occurred_at,
            utilisateur_id=audit_log.utilisateur_id,
            ressource_kind=audit_log.ressource_kind,
            ressource_id=audit_log.ressource_id,
            event_name=audit_log.event_name,
        )
