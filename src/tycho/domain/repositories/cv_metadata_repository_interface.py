"""CV metadata repository interface."""

from typing import Optional, Protocol
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata


class ICVMetadataRepository(Protocol):
    """Interface for CV metadata repository operations."""

    def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        """Save CV metadata to repository.

        Args:
            cv_metadata: CVMetadata entity to save

        Returns:
            Saved CVMetadata entity

        Raises:
            RepositoryError: If save operation fails
        """
        ...

    def find_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        """Find CV metadata by ID.

        Args:
            cv_id: id of the CV metadata

        Returns:
            CVMetadata entity if found, None otherwise

        Raises:
            RepositoryError: If query operation fails
        """
        ...
