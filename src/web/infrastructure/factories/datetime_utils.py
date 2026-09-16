from datetime import date, datetime, timezone

from django.utils import timezone as django_timezone


def date_to_aware_datetime(d: date, hour: int = 12) -> datetime:
    return datetime(d.year, d.month, d.day, hour, 0, 0, tzinfo=timezone.utc)


def as_aware(value: datetime | None) -> datetime | None:
    # Les fabriques acceptent les deux formes : une date deja consciente passe
    # telle quelle, une date naive est rattachee au fuseau courant de Django.
    if value is None or django_timezone.is_aware(value):
        return value
    return django_timezone.make_aware(value)
