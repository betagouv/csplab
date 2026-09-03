"""Minimal reimplementation of django.db.models.TextChoices.

referentiel is consumed by services that do not depend on Django (e.g.
ingestion), so it must not import django itself. This mirrors the subset of
Django's TextChoices API actually used across the codebase (member.label,
Cls.choices/labels/values, str(member) == member.value) without the
dependency.
"""

from enum import Enum, EnumType


class ChoicesType(EnumType):
    """Adds ``.choices`` / ``.labels`` / ``.values`` class-level properties."""

    @property
    def choices(cls):
        return [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [member.label for member in cls]

    @property
    def values(cls):
        return [member.value for member in cls]


class TextChoices(str, Enum, metaclass=ChoicesType):
    """String enum exposing ``.label`` per member and ``.choices`` on the class."""

    def __new__(cls, value, label):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"
