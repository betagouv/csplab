from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from infrastructure.django_apps.ingestion.models.api_log import ApiLogModel


class ApiLogModelFactory:
    @staticmethod
    def create_model(
        path: str = "/api/v1/offres/",
        method: str = "GET",
        token_type: Optional[str] = "jwt",  # noqa: S107
        timestamp: Optional[datetime] = None,
        ip_address: str = "127.0.0.1",
        status_code: int = 200,
        auth_token: Optional[str] = "test-token",  # noqa: S107
    ) -> ApiLogModel:
        model = ApiLogModel(
            id=uuid4(),
            path=path,
            method=method,
            token_type=token_type,
            timestamp=timestamp or datetime.now(tz=timezone.utc),
            ip_address=ip_address,
            status_code=status_code,
            auth_token=auth_token,
        )
        model.save()
        return model
