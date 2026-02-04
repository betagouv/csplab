"""Factory for CV-related test data."""

from datetime import UTC, datetime
from uuid import uuid4

from domain.value_objects.cv_processing_status import CVStatus
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


class CVMetadataModelFactory:
    """Factory for CVMetadataModel Django model."""

    @classmethod
    def build(cls, **kwargs: object) -> CVMetadataModel:
        """Build a CVMetadataModel instance without saving to database."""
        now = datetime.now(tz=UTC)
        defaults: dict[str, object] = {
            "id": uuid4(),
            "filename": f"cv_{uuid4().hex[:8]}.pdf",
            "status": CVStatus.COMPLETED.value,
            "created_at": now,
            "updated_at": now,
            "extracted_text": {"pages": ["Expérience professionnelle", "Formation"]},
            "search_query": "Développeur Python Django",
        }
        defaults.update(kwargs)
        return CVMetadataModel(**defaults)

    @classmethod
    def create(cls, **kwargs: object) -> CVMetadataModel:
        """Create and save a CVMetadataModel instance to database."""
        instance = cls.build(**kwargs)
        instance.save()
        return instance
