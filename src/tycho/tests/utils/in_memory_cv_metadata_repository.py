"""In-memory implementation of CV metadata repository for testing."""

from typing import Dict, Optional
from uuid import UUID

from domain.entities.cv_metadata import CVMetadata
from domain.repositories.cv_metadata_repository_interface import ICVMetadataRepository


class InMemoryCVMetadataRepository(ICVMetadataRepository):
    """In-memory implementation of CV metadata repository for testing."""

    def __init__(self):
        """Initialize the repository with empty storage."""
        self._storage: Dict[UUID, CVMetadata] = {}

    def save(self, cv_metadata: CVMetadata) -> CVMetadata:
        """Save CV metadata to in-memory storage.

        Args:
            cv_metadata: CVMetadata entity to save

        Returns:
            Saved CVMetadata entity

        Raises:
            RepositoryError: If save operation fails
        """
        self._storage[cv_metadata.id] = cv_metadata
        return cv_metadata

    def find_by_id(self, cv_id: UUID) -> Optional[CVMetadata]:
        """Find CV metadata by ID in memory storage.

        Args:
            cv_id: id of the CV metadata

        Returns:
            CVMetadata entity if found, None otherwise

        Raises:
            RepositoryError: If query operation fails
        """
        return self._storage.get(cv_id)

    def clear(self):
        """Clear all stored CV metadata (for testing purposes)."""
        self._storage.clear()

    def count(self) -> int:
        """Return the number of stored CV metadata (for testing purposes)."""
        return len(self._storage)
