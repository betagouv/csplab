import logging
import uuid
from uuid import UUID

from django.db import models, transaction
from django.db.models import Q
from django.utils import timezone

from config.logger_names import LoggerName
from domain.commons.entities.audit_log import AuditLog
from infrastructure.django_apps.commons.enums import Canal, Resultat
from infrastructure.django_apps.utils.ip import IPAddressInput, parse_ip
from infrastructure.django_apps.utils.models import BaseDatedModel

logger = logging.getLogger(LoggerName.IDENTITE)


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


class AuditLoginLogQuerySet(models.QuerySet):
    def record_attempt(
        self,
        *,
        canal: Canal,
        resultat: Resultat,
        utilisateur_id: UUID | None = None,
        ip_address: IPAddressInput | None = None,
    ) -> None:
        parsed_ip = parse_ip(ip_address)
        if ip_address and parsed_ip is None:
            logger.warning("Unparseable client IP in login audit.")
        try:
            with transaction.atomic():
                self.create(
                    canal=canal,
                    resultat=resultat,
                    utilisateur_id=utilisateur_id,
                    ip_address=parsed_ip,
                )
        except Exception as e:
            logger.error("Failed to record login attempt: %s", type(e).__name__)


class AuditLoginLogModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)
    utilisateur_id = models.UUIDField(null=True, blank=True, db_index=True)
    canal = models.CharField(max_length=20, choices=Canal.choices)
    resultat = models.CharField(max_length=10, choices=Resultat.choices)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    objects = AuditLoginLogQuerySet.as_manager()

    class Meta:
        db_table = "audit_login_logs"
        ordering = ["-occurred_at"]
        constraints = [
            models.CheckConstraint(
                condition=~Q(resultat=Resultat.SUCCES)
                | Q(utilisateur_id__isnull=False)
                | Q(canal=Canal.APIKEY),
                name="audit_login_logs_succes_has_user",
            ),
        ]

    def __str__(self):
        return f"{self.canal} {self.resultat} {self.occurred_at:%Y-%m-%d %H:%M:%S}"
