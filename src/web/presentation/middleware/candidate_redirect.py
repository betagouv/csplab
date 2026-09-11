from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

CANDIDATE_URL_PREFIX = "/candidate/"
CANDIDATE_EXTERNAL_REDIRECT_URL = "https://choisirleservicepublic.gouv.fr/nos-offres/"


class CandidateRedirectMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not request.path.startswith(CANDIDATE_URL_PREFIX):
            return self.get_response(request)

        if request.headers.get("HX-Request"):
            response = HttpResponse()
            response["HX-Redirect"] = CANDIDATE_EXTERNAL_REDIRECT_URL
            return response

        return redirect(CANDIDATE_EXTERNAL_REDIRECT_URL, preserve_request=True)
