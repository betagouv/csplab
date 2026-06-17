from django.db import models

from domain.audit.entities.audit_log import AuditLog
from infrastructure.django_apps.utils.models import BaseDatedModel


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
