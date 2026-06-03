from ddd.types import JsonDataType

from domain.candidate.exceptions.cv_errors import QueryBuildingError
from domain.candidate.services.query_builder_interface import IQueryBuilder


class QueryBuilder(IQueryBuilder):
    def build_query(self, cv_data: JsonDataType) -> str:
        if not cv_data or not isinstance(cv_data, dict):
            raise QueryBuildingError("CV data cannot be empty or invalid")

        keywords = []

        experiences = cv_data.get("experiences", [])
        if isinstance(experiences, list):
            for exp in experiences:
                if isinstance(exp, dict):
                    title = exp.get("title", "")
                    if isinstance(title, str) and title:
                        keywords.append(title.lower())

        unique_keywords = list(set(keywords))
        return " ".join(unique_keywords)
