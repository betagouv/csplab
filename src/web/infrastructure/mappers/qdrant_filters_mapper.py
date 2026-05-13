from typing import Optional, cast

from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from domain.interfaces.mapper_interface import IFromDomainMapper
from domain.repositories.vector_repository_interface import IFilters


class QdrantFiltersMapper(IFromDomainMapper[IFilters, Filter]):
    def _extract_value(self, item):
        if hasattr(item, "code"):
            return item.code
        elif hasattr(item, "value"):
            return item.value
        else:
            return str(item)

    def from_domain(self, filters: Optional[IFilters]) -> Optional[Filter]:
        if not filters:
            return None

        qdrant_filters = {}

        doc_type = filters.get("document_type")
        if doc_type:
            qdrant_filters["document_type"] = doc_type

        verse = filters.get("verse")
        if verse:
            qdrant_filters["verse"] = verse

        category = filters.get("category")
        if category:
            qdrant_filters["category"] = category

        region = filters.get("region")
        if region:
            qdrant_filters["localisation.region"] = region

        department = filters.get("department")
        if department:
            qdrant_filters["localisation.department"] = department

        country = filters.get("country")
        if country:
            qdrant_filters["localisation.country"] = country

        must_conditions = []
        for key, value in qdrant_filters.items():
            if isinstance(value, list):
                should_conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=cast(str, self._extract_value(item))),
                    )
                    for item in value
                ]
                must_conditions.append(Filter(should=cast(list, should_conditions)))
            else:
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=cast(str, self._extract_value(value))),
                    )
                )

        return Filter(must=cast(list, must_conditions)) if must_conditions else None
