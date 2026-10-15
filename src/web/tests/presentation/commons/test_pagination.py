from unittest.mock import MagicMock

import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from presentation.commons.pagination import (
    MAX_PAGE_SIZE,
    TalentsoftPagination,
    WebPagination,
)


def _request(query: str) -> Request:
    return Request(APIRequestFactory().get(f"/api/?{query}"))


def _page(total: int = 5_000) -> MagicMock:
    page = MagicMock()
    page.count.return_value = total
    page.slice.return_value = []
    return page


def test_get_schema_operation_parameters_exposes_page_and_size():
    parameters = WebPagination().get_schema_operation_parameters(view=None)

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
                "default": WebPagination.page_size,
                "minimum": WebPagination.min_page_size,
                "maximum": WebPagination.max_page_size,
            },
        },
    ]


def test_get_paginated_response_schema_wraps_results():
    results_schema = {"type": "string"}

    schema = WebPagination().get_paginated_response_schema(results_schema)

    assert schema == {
        "type": "object",
        "required": ["count", "results"],
        "properties": {
            "count": {"type": "integer", "example": 1},
            "next": {
                "type": "string",
                "format": "uri",
                "nullable": True,
                "example": None,
            },
            "previous": {
                "type": "string",
                "format": "uri",
                "nullable": True,
                "example": None,
            },
            "results": results_schema,
        },
    }


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
    "query,expected_size,expected_page",
    [
        ("", WebPagination.page_size, 1),
        ("taille=50&page=3", 50, 3),
        (f"taille={MAX_PAGE_SIZE}", MAX_PAGE_SIZE, 1),
        ("taille=1000000", MAX_PAGE_SIZE, 1),
        ("taille=0", WebPagination.page_size, 1),
        ("taille=-5", WebPagination.page_size, 1),
        ("taille=abc", WebPagination.page_size, 1),
        ("page=0", WebPagination.page_size, 1),
        ("page=-2", WebPagination.page_size, 1),
        ("page=abc", WebPagination.page_size, 1),
    ],
)
def test_web_pagination_bounds_size_and_page(query, expected_size, expected_page):
    paginator = WebPagination()
    page = _page()

    paginator.paginate(page, _request(query))

    assert paginator.page_size == expected_size
    assert paginator.page_num == expected_page
    page.slice.assert_called_once_with(
        (expected_page - 1) * expected_size, expected_size
    )


def test_web_pagination_next_url_uses_capped_size():
    paginator = WebPagination()

    paginator.paginate(_page(), _request("taille=1000000"))

    assert f"taille={MAX_PAGE_SIZE}" in paginator._get_next_url()


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
