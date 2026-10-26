from typing import Any

from ddd.page_interface import IPage
from rest_framework.pagination import (
    BasePagination,
    CursorPagination,
    PageNumberPagination,
)
from rest_framework.response import Response

MAX_PAGE_SIZE = 1_000


def _bounded_int(
    raw: str | None, default: int, minimum: int, maximum: int | None
) -> int:
    try:
        value = int(raw) if raw is not None else default
    except ValueError:
        return default
    if value < minimum:
        return default
    if maximum is not None:
        return min(value, maximum)
    return value


def _page_taille_parameters(page_size: int | None, max_page_size: int) -> list[dict]:
    return [
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
                "default": page_size,
                "minimum": 1,
                "maximum": max_page_size,
            },
        },
    ]


class PageNumberLimitPagination(PageNumberPagination):
    page_size_query_param = "limit"
    max_page_size = MAX_PAGE_SIZE


class LatestMessagesCursorPagination(CursorPagination):
    """Serves the latest messages, oldest first; `next` leads to older ones."""

    ordering = ("-created_at", "-id")
    page_size = 25
    max_page_size = 100
    page_size_query_param = "limit"

    def get_paginated_response(self, data: list[Any]) -> Response:
        return super().get_paginated_response(list(reversed(data)))


class TaillePageNumberPagination(PageNumberPagination):
    page_size_query_param = "taille"
    max_page_size = MAX_PAGE_SIZE

    def get_schema_operation_parameters(self, view) -> list[dict]:
        return _page_taille_parameters(self.page_size, self.max_page_size)

    def get_paginated_response_schema(self, schema: dict) -> dict:
        return {
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
                "results": schema,
            },
        }


class TalentsoftPagination(BasePagination):
    start_default = 0
    count_default = 100
    count_max = MAX_PAGE_SIZE

    def paginate(self, page: IPage, request) -> list[Any]:
        self.start = _bounded_int(
            request.query_params.get("start"),
            default=self.start_default,
            minimum=0,
            maximum=None,
        )
        self.count = _bounded_int(
            request.query_params.get("count"),
            default=self.count_default,
            minimum=1,
            maximum=self.count_max,
        )
        self.total = page.count()
        self.results = list(page.slice(self.start, self.count))

        return self.results

    def get_paginated_response(self, data: list[Any]) -> Response:
        return Response(
            {
                "data": data,
                "_pagination": {
                    "start": self.start,
                    "count": len(self.results),
                    "total": self.total,
                    "resultsPerPage": self.count,
                    "hasMore": self.start + len(self.results) < self.total,
                },
            }
        )

    def get_schema_operation_parameters(self, view) -> list[dict]:
        return [
            {
                "name": "start",
                "required": False,
                "in": "query",
                "description": "Index de début de la pagination.",
                "schema": {
                    "type": "integer",
                    "default": self.start_default,
                    "minimum": 0,
                },
            },
            {
                "name": "count",
                "required": False,
                "in": "query",
                "description": "Nombre d'éléments par page.",
                "schema": {
                    "type": "integer",
                    "default": self.count_default,
                    "minimum": 1,
                    "maximum": self.count_max,
                },
            },
        ]

    def get_paginated_response_schema(self, schema: dict) -> dict:
        return {
            "type": "object",
            "required": ["data", "_pagination"],
            "properties": {
                "data": schema,
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
