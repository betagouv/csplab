from dataclasses import dataclass
from datetime import datetime, timezone

from domain.exceptions.offer_errors import InvalidLimitDateError


@dataclass(frozen=True)
class LimitDate:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise InvalidLimitDateError(self.value)

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc) > self.value
