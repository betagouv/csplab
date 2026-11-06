from django.http import HttpResponse, HttpResponseBase
from django.template.response import SimpleTemplateResponse
from django.utils.cache import (
    get_conditional_response,
    patch_cache_control,
    set_response_etag,
)
from rest_framework import status
from rest_framework.request import Request


class ConditionalGetMixin:
    def finalize_response(
        self, request: Request, response: HttpResponseBase, *args, **kwargs
    ) -> HttpResponseBase:
        response = super().finalize_response(  # type: ignore[misc]
            request, response, *args, **kwargs
        )
        if request.method != "GET" or response.status_code != status.HTTP_200_OK:
            return response
        patch_cache_control(response, private=True, no_cache=True)
        if isinstance(response, SimpleTemplateResponse):
            response.add_post_render_callback(
                lambda rendered: _not_modified_if_unchanged(request, rendered)
            )
        return response


def _not_modified_if_unchanged(
    request: Request, response: HttpResponse
) -> HttpResponseBase | None:
    set_response_etag(response)
    if not response.has_header("ETag"):
        return None
    return get_conditional_response(request, etag=response["ETag"], response=response)
