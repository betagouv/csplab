"""Query builder implementation."""

from typing import Any, Dict

from core.services.query_builder_interface import IQueryBuilder
from domain.exceptions.cv_errors import QueryBuildingError


class QueryBuilder(IQueryBuilder):
    """Implementation of query building service."""

    def build_query(self, cv_data: Dict[str, Any]) -> str:
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
                }

        Returns:
            Optimized search query string for semantic search

        Raises:
            QueryBuildingError: If CV data is empty or invalid
        """
        if not cv_data or not isinstance(cv_data, dict):
            raise QueryBuildingError("CV data cannot be empty or invalid")

        keywords = []

        experiences = cv_data.get("experiences", [])
        if isinstance(experiences, list):
            for exp in experiences:
                if isinstance(exp, dict):
                    title = exp.get("title", "").lower()
                    keywords.append(title)

        unique_keywords = list(set(keywords))
        return " ".join(unique_keywords)
