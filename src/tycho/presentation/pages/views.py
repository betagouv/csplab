from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/home.html"


def custom_403_view(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    return render(request, "403.html", status=HTTPStatus.FORBIDDEN)


def custom_404_view(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    return render(request, "404.html", status=HTTPStatus.NOT_FOUND)


def custom_500_view(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    return render(request, "500.html", status=HTTPStatus.INTERNAL_SERVER_ERROR)
