"""Django implementation of CV metadata repository."""

from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from apps.candidate.infrastructure.adapters.persistence.models.cv_metadata import (
    CVMetadataModel,
)
from core.entities.cv_metadata import CVMetadata
from core.repositories.cv_metadata_repository_interface import ICVMetadataRepository


class CVMetadataRepository(ICVMetadataRepository):
    """Django ORM implementation of CV metadata repository."""

    def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        """Save CV metadata to database.

        Args:
            cv_metadata: CVMetadata entity to save

        Returns:
            Saved CVMetadata entity

        Raises:
            RepositoryError: If save operation fails
        """
        model = CVMetadataModel.from_entity(cv_metadata)
        model.save()
        return model.to_entity()

    def find_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        """Find CV metadata by ID.

        Args:
            cv_id: id of the CV metadata

        Returns:
            CVMetadata entity if found, None otherwise

        Raises:
            RepositoryError: If query operation fails
        """
        try:
            model = CVMetadataModel.objects.get(id=cv_id)
            return model.to_entity()
        except ObjectDoesNotExist:
            return None
