from django.db import models

from domain.ingestion.entities.api_log import ApiLog


class ApiLogModel(models.Model):
    id = models.UUIDField(primary_key=True)
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=2048)
    ip_address = models.GenericIPAddressField()
    method = models.CharField(max_length=10)
    status_code = models.PositiveSmallIntegerField()
    auth_token = models.TextField(null=True, blank=True)
    token_type = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = "api_logs"
        verbose_name = "API Log"
        verbose_name_plural = "API Logs"
        indexes = [
            models.Index(fields=["timestamp"], name="api_logs_timestamp_idx"),
            models.Index(fields=["path"], name="api_logs_path_idx"),
            models.Index(fields=["ip_address"], name="api_logs_ip_address_idx"),
            models.Index(fields=["token_type"], name="api_logs_token_type_idx"),
        ]

    def to_entity(self) -> ApiLog:
        return ApiLog(
            id=self.id,
            timestamp=self.timestamp,
            path=self.path,
            ip_address=self.ip_address,
            method=self.method,
            status_code=self.status_code,
            auth_token=self.auth_token,
            token_type=self.token_type,
        )

    @classmethod
    def from_entity(cls, api_log: ApiLog) -> "ApiLogModel":
        return cls(
            id=api_log.id,
            timestamp=api_log.timestamp,
            path=api_log.path,
            ip_address=api_log.ip_address,
            method=api_log.method,
            status_code=api_log.status_code,
            auth_token=api_log.auth_token,
            token_type=api_log.token_type,
        )
