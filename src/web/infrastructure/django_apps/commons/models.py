from django.db import models

from domain.commons.entities.audit_log import AuditLog
from infrastructure.django_apps.utils.models import BaseDatedModel


class StatSnapshotModel(models.Model):
    pk = models.CompositePrimaryKey("date", "metric_name")
    date = models.DateField()
    metric_name = models.CharField(max_length=255)
    metric_value = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "stat_snapshots"
        verbose_name = "Stat Snapshot"
        verbose_name_plural = "Stat Snapshots"
        ordering = ["-date"]


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
