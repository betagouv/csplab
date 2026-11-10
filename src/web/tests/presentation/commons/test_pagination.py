from unittest.mock import MagicMock

import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from presentation.commons.pagination import (
    MAX_PAGE_SIZE,
    TaillePageNumberPagination,
    TalentsoftPagination,
)


def _request(query: str) -> Request:
    return Request(APIRequestFactory().get(f"/api/?{query}"))


def _page(total: int = 5_000) -> MagicMock:
    page = MagicMock()
    page.count.return_value = total
    page.slice.return_value = []
    return page


def test_get_schema_operation_parameters_exposes_page_and_size():
    parameters = TaillePageNumberPagination().get_schema_operation_parameters(view=None)

    assert parameters == [
        {
            "name": "page",
            "required": False,
            "in": "query",
            "description": "Numéro de la page.",
            "schema": {"type": "integer", "default": 1, "minimum": 1},
        },
        {
            "name": "taille",
            "required": False,
            "in": "query",
            "description": "Nombre d'éléments par page.",
            "schema": {
                "type": "integer",
                "default": TaillePageNumberPagination.page_size,
                "minimum": 1,
                "maximum": MAX_PAGE_SIZE,
            },
        },
    ]


def test_talentsoft_get_schema_operation_parameters_exposes_start_and_count():
    parameters = TalentsoftPagination().get_schema_operation_parameters(view=None)

    assert parameters == [
        {
            "name": "start",
            "required": False,
            "in": "query",
            "description": "Index de début de la pagination.",
            "schema": {"type": "integer", "default": 0, "minimum": 0},
        },
        {
            "name": "count",
            "required": False,
            "in": "query",
            "description": "Nombre d'éléments par page.",
            "schema": {
                "type": "integer",
                "default": 100,
                "minimum": 1,
                "maximum": MAX_PAGE_SIZE,
            },
        },
    ]


def test_talentsoft_get_paginated_response_schema_wraps_results():
    results_schema = {"type": "string"}

    schema = TalentsoftPagination().get_paginated_response_schema(results_schema)

    assert schema == {
        "type": "object",
        "required": ["data", "_pagination"],
        "properties": {
            "data": results_schema,
            "_pagination": {
                "type": "object",
                "properties": {
                    "start": {"type": "integer", "example": 0},
                    "count": {"type": "integer", "example": 1},
                    "total": {"type": "integer", "example": 1},
                    "resultsPerPage": {"type": "integer", "example": 100},
                    "hasMore": {"type": "boolean", "example": False},
                },
            },
        },
    }


@pytest.mark.parametrize(
    "query,expected_start,expected_count",
    [
        ("", 0, 100),
        ("start=200&count=50", 200, 50),
        ("count=1000000", 0, MAX_PAGE_SIZE),
        ("count=0", 0, 100),
        ("count=abc", 0, 100),
        ("start=-1", 0, 100),
        ("start=abc", 0, 100),
    ],
)
def test_talentsoft_pagination_bounds_start_and_count(
    query, expected_start, expected_count
):
    paginator = TalentsoftPagination()
    page = _page()

    paginator.paginate(page, _request(query))

    assert paginator.start == expected_start
    assert paginator.count == expected_count
    page.slice.assert_called_once_with(expected_start, expected_count)
