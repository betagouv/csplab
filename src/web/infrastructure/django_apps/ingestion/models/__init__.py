"""Ingestion infrastructure models implementations."""

from infrastructure.django_apps.ingestion.models.raw_document import RawDocument
from infrastructure.django_apps.ingestion.models.source import SourceModel

__all__ = ["RawDocument", "SourceModel"]
