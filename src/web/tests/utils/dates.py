from datetime import datetime

from rest_framework.fields import DateTimeField


def parse_datetime(raw: str) -> datetime:
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def datetime_to_str(dt: datetime) -> str:
    return dt.isoformat(timespec="microseconds").replace("+00:00", "Z")


def datetime_to_drf_representation(dt: datetime) -> str:
    return DateTimeField().to_representation(dt)
