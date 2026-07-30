from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from ddd.page_interface import IPage
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from rest_framework.settings import api_settings


class WebPagination(BasePagination):
    page_size = api_settings.PAGE_SIZE

    def paginate(self, page: IPage, request) -> list[Any]:
        self.request = request
        self.count = page.count()
        self.page_size = int(self.request.query_params.get("size", self.page_size))
        self.page_num = int(self.request.query_params.get("page", 1))

        offset = (self.page_num - 1) * self.page_size
        self.results = list(page.slice(offset, self.page_size))

        return self.results

    def get_paginated_response(self, data: list[Any]) -> Response:
        return Response(
            {
                "count": self.count,
                "next": self._get_next_url(),
                "previous": self._get_previous_url(),
                "results": data,
            }
        )

    def get_schema_operation_parameters(self, view) -> list[dict]:
        return [
            {
                "name": "page",
                "required": False,
                "in": "query",
                "description": "Numéro de la page.",
                "schema": {"type": "integer"},
            },
            {
                "name": "size",
                "required": False,
                "in": "query",
                "description": "Nombre d'éléments par page.",
                "schema": {"type": "integer"},
            },
        ]

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

    def _get_next_url(self):
        if self.page_num * self.page_size >= self.count:
            return None
        return self._build_url(self.page_num + 1)

    def _get_previous_url(self):
        if self.page_num <= 1:
            return None
        return self._build_url(self.page_num - 1)

    def _build_url(self, page_num):
        request = self.request
        url = request.build_absolute_uri()
        parsed = urlparse(url)
        params = parse_qs(parsed.query, keep_blank_values=True)
        params["page"] = [page_num]
        params["size"] = [self.page_size]
        new_query = urlencode({k: v[0] for k, v in params.items()})
        return urlunparse(parsed._replace(query=new_query))


class TalentsoftPagination(BasePagination):
    start_default = 0
    count_default = 100

    def paginate(self, page: IPage, request) -> list[Any]:
        self.start = int(request.query_params.get("start", self.start_default))
        self.count = int(request.query_params.get("count", self.count_default))
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
                "schema": {"type": "integer"},
            },
            {
                "name": "count",
                "required": False,
                "in": "query",
                "description": "Nombre d'éléments par page.",
                "schema": {"type": "integer"},
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
