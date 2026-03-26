from typing import Optional, cast

from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from domain.interfaces.mapper_interface import IFromDomainMapper
from domain.repositories.vector_repository_interface import IFilters


class QdrantFiltersMapper(IFromDomainMapper[IFilters, Filter]):
    def from_domain(self, filters: Optional[IFilters]) -> Optional[Filter]:
        if not filters:
            return None

        qdrant_filters = {}

        document_type = filters.get("document_type")
        if document_type:
            qdrant_filters["document_type"] = document_type

        verse = filters.get("verse")
        if verse:
            qdrant_filters["verse"] = verse

        must_conditions = []
        for key, value in qdrant_filters.items():
            if isinstance(value, list):
                should_conditions = [
                    FieldCondition(
                        key=key,
                        match=MatchValue(
                            value=cast(
                                str, item.value if hasattr(item, "value") else item
                            )
                        ),
                    )
                    for item in value
                ]
                must_conditions.append(Filter(should=cast(list, should_conditions)))
            else:
                must_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(
                            value=cast(
                                str, value.value if hasattr(value, "value") else value
                            )
                        ),
                    )
                )

        return Filter(must=cast(list, must_conditions)) if must_conditions else None
