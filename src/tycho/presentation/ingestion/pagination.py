from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings


class OffersPagination(PageNumberPagination):
    page_size = api_settings.PAGE_SIZE
    page_size_query_param = "size"
    max_page_size = api_settings.PAGE_SIZE
    page_query_param = "page"
