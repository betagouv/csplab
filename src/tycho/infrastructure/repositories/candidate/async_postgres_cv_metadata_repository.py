"""Async Django implementation of CV metadata repository using native async ORM."""

from typing import Optional
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist

from domain.entities.cv_metadata import CVMetadata
from domain.exceptions.cv_errors import CVNotFoundError
from domain.repositories.async_cv_metadata_repository_interface import (
    IAsyncCVMetadataRepository,
)
from infrastructure.django_apps.candidate.models.cv_metadata import CVMetadataModel


class AsyncPostgresCVMetadataRepository(IAsyncCVMetadataRepository):
    """Async Django ORM implementation using native async methods."""

    async def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        """Save CV metadata to database asynchronously using Django async ORM.

        Args:
            cv_metadata: CVMetadata entity to save

        Returns:
            Saved CVMetadata entity

        Raises:
            RepositoryError: If save operation fails
        """
        model = CVMetadataModel.from_entity(cv_metadata)
        await model.asave()
        return model.to_entity()

    async def find_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        """Find CV metadata by ID asynchronously using Django async ORM.

        Args:
            cv_id: id of the CV metadata

        Returns:
            CVMetadata entity if found, None otherwise

        Raises:
            RepositoryError: If query operation fails
        """
        try:
            model = await CVMetadataModel.objects.aget(id=cv_id)
            return model.to_entity()
        except ObjectDoesNotExist as e:
            raise CVNotFoundError(str(cv_id)) from e

    def count(self) -> int:
        """Count total CV metadata records.

        Note: Using sync count as it's typically used in tests/admin contexts.

        Returns:
            Total number of CV metadata records

        Raises:
            RepositoryError: If count operation fails
        """
        return CVMetadataModel.objects.count()
