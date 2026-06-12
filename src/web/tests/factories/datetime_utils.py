from datetime import date, datetime, timezone


def date_to_aware_datetime(d: date, hour: int = 12) -> datetime:
    return datetime(d.year, d.month, d.day, hour, 0, 0, tzinfo=timezone.utc)
