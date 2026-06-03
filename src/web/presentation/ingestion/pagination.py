from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from ddd.page_interface import IPage
from rest_framework.pagination import BasePagination
from rest_framework.response import Response
from rest_framework.settings import api_settings


class IngestionPagination(BasePagination):
    page_size = api_settings.PAGE_SIZE

    def paginate(self, page: IPage, request):
        self.request = request
        self.count = page.count()
        self.page_size = int(self.request.query_params.get("size", self.page_size))
        self.page_num = int(self.request.query_params.get("page", 1))

        offset = (self.page_num - 1) * self.page_size
        self.results = list(page.slice(offset, self.page_size))

        return self.results

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.count,
                "next": self._get_next_url(),
                "previous": self._get_previous_url(),
                "results": data,
            }
        )

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
