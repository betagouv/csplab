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

        qdrant_filters: dict[str, list[str]] = {}

        filter_handlers = {
            "localisation": self._handle_localisation_filter,
            "opportunity_type": self._handle_opportunity_type_filter,
            "verse": self._handle_verse_filter,
            "category": self._handle_category_filter,
        }

        for filter_type, filter_values in filters.items():
            if not filter_values:
                continue

            handler = filter_handlers.get(filter_type)
            if handler:
                handler(filter_values, qdrant_filters)

        if not qdrant_filters:
            return None

        must_conditions = []
        for key, value in qdrant_filters.items():
            if isinstance(value, list):
                should_conditions = [
                    FieldCondition(key=key, match=MatchValue(value=item))
                    for item in value
                ]
                must_conditions.append(Filter(should=cast(list, should_conditions)))
            else:
                must_conditions.append(
                    Filter(
                        must=[FieldCondition(key=key, match=MatchValue(value=value))]
                    )
                )
        return Filter(must=cast(list, must_conditions)) if must_conditions else None

    def _handle_localisation_filter(self, filter_values, qdrant_filters):
        departments = []
        regions = []
        countries = []

        for loc in filter_values:
            if hasattr(loc, "department") and hasattr(loc.department, "code"):
                departments.append(loc.department.code)
            if hasattr(loc, "region") and hasattr(loc.region, "code"):
                regions.append(loc.region.code)
            if hasattr(loc, "country") and hasattr(loc.country, "code"):
                countries.append(loc.country.code)

        if departments:
            qdrant_filters["department"] = departments
        if regions:
            qdrant_filters["region"] = regions
        if countries:
            qdrant_filters["country"] = countries

    def _handle_opportunity_type_filter(self, filter_values, qdrant_filters):
        doc_types = []
        for opp_type in filter_values:
            if hasattr(opp_type, "value"):
                if opp_type.value == "CONCOURS":
                    doc_types.append("CONCOURS")
                elif opp_type.value == "OFFER":
                    doc_types.append("OFFERS")
        if doc_types:
            qdrant_filters["document_type"] = doc_types

    def _handle_verse_filter(self, filter_values, qdrant_filters):
        verses = []
        for verse in filter_values:
            if hasattr(verse, "value"):
                verses.append(verse.value)
        if verses:
            qdrant_filters["verse"] = verses

    def _handle_category_filter(self, filter_values, qdrant_filters):
        categories = []
        for category in filter_values:
            if hasattr(category, "value"):
                categories.append(category.value)
        if categories:
            qdrant_filters["category"] = categories
