import hashlib
import os
from collections.abc import Callable

from django.http import HttpResponse, HttpResponseBase
from django.template.response import SimpleTemplateResponse
from django.utils.cache import (
    get_conditional_response,
    patch_cache_control,
    set_response_etag,
)
from django.utils.http import quote_etag
from rest_framework import status
from rest_framework.request import Request

# Scalingo exposes the deployed version: a deploy may change the response format.
DEPLOYED_VERSION = os.environ.get("CONTAINER_VERSION", "")


class ConditionalGetMixin:
    def finalize_response(
        self, request: Request, response: HttpResponseBase, *args, **kwargs
    ) -> HttpResponseBase:
        response = super().finalize_response(  # type: ignore[misc]
            request, response, *args, **kwargs
        )
        if request.method != "GET" or response.status_code not in (
            status.HTTP_200_OK,
            status.HTTP_304_NOT_MODIFIED,
        ):
            return response
        patch_cache_control(response, private=True, no_cache=True)
        if isinstance(response, SimpleTemplateResponse):
            response.add_post_render_callback(
                lambda rendered: _not_modified_if_unchanged(request, rendered)
            )
        return response

    def respond_unless_unchanged(
        self, request: Request, version: object, build: Callable[[], HttpResponseBase]
    ) -> HttpResponseBase:
        etag = _etag(request, version)
        response = get_conditional_response(request, etag=etag) or build()
        if response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_304_NOT_MODIFIED,
        ):
            response["ETag"] = etag
        return response


def _etag(request: Request, version: object) -> str:
    key = repr((DEPLOYED_VERSION, request.user.pk, request.get_full_path(), version))
    return quote_etag(hashlib.sha256(key.encode()).hexdigest())


def _not_modified_if_unchanged(
    request: Request, response: HttpResponse
) -> HttpResponseBase | None:
    if not response.has_header("ETag"):
        set_response_etag(response)
    if not response.has_header("ETag"):
        return None
    return get_conditional_response(request, etag=response["ETag"], response=response)
