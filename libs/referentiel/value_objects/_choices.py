"""Minimal reimplementation of django.db.models.TextChoices.

referentiel is consumed by services that do not depend on Django (e.g.
ingestion), so it must not import django itself. This mirrors the subset of
Django's TextChoices API actually used across the codebase (member.label,
Cls.choices/labels/values, str(member) == member.value) without the
dependency.
"""

import enum
from enum import EnumType
from enum import property as enum_property


class ChoicesType(EnumType):
    """Metaclass turning ``NAME = "value", "label"`` members into a choices enum."""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if isinstance(value, (list, tuple)) and len(value) > 1:
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace("_", " ").title()
            labels.append(label)
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels, strict=True):
            member._label_ = label
        return enum.unique(cls)

    @property
    def choices(cls):
        return [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


class TextChoices(str, enum.Enum, metaclass=ChoicesType):
    """String enum exposing ``.label`` per member and ``.choices`` on the class."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name

    @enum_property
    def label(self):
        return self._label_

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"
