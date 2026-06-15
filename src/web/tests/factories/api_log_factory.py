from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.ingestion.entities.api_log import ApiLog


class ApiLogFactory:
    @staticmethod
    def create_entity(
        id: Optional[UUID] = None,
        timestamp: Optional[datetime] = None,
        path: str = "/api/v1/offres/",
        ip_address: str = "127.0.0.1",
        method: str = "GET",
        status_code: int = 200,
        auth_token: Optional[str] = "test-token",  # noqa: S107
        token_type: Optional[str] = "jwt",  # noqa: S107
    ) -> ApiLog:
        return ApiLog(
            id=id or uuid4(),
            timestamp=timestamp or datetime.now(tz=timezone.utc),
            path=path,
            ip_address=ip_address,
            method=method,
            status_code=status_code,
            auth_token=auth_token,
            token_type=token_type,
        )
