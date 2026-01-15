"""Async CV metadata repository interface."""

from typing import Optional, Protocol
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata


class IAsyncCVMetadataRepository(Protocol):
    """Async interface for CV metadata repository operations."""

    async def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        """Save CV metadata to repository asynchronously.

        Args:
            cv_metadata: CVMetadata entity to save

        Returns:
            Saved CVMetadata entity

        Raises:
            RepositoryError: If save operation fails
        """
        ...

    async def find_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        """Find CV metadata by ID asynchronously.

        Args:
            cv_id: id of the CV metadata

        Returns:
            CVMetadata entity if found, None otherwise

        Raises:
            RepositoryError: If query operation fails
        """
        ...

    def count(self) -> int:
        """Count total CV metadata records.

        Returns:
            Total number of CV metadata records

        Raises:
            RepositoryError: If count operation fails
        """
        ...
