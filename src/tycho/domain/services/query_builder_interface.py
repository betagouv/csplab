"""Query builder interface for constructing search queries from CV data."""

from typing import Protocol

from domain.types import JsonDataType


class IQueryBuilder(Protocol):
    """Interface for building search queries from CV structured data."""

    def build_query(self, cv_data: JsonDataType) -> str:
        """Build a search query from CV structured data.

        Args:
            cv_data: Structured CV data with format:
                {
                    "experiences": [
                            {
                                "title": str, "company": str,
                                "sector": str|None,
                                "description": str
                            }
                        ]
                    "skills": [str, ...],
                }

        Returns:
            Optimized search query string for semantic search

        Raises:
            QueryBuildingError: If CV data is empty or invalid
        """
        ...
