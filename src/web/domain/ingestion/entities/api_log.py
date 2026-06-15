from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class ApiLog:
    id: UUID
    timestamp: datetime
    path: str
    ip_address: str
    method: str
    status_code: int
    auth_token: Optional[str]
    token_type: Optional[str]
