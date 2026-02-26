"""URL configuration for tycho project."""

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from presentation.api import urls as api_urls
from presentation.pages.views import custom_403_view, custom_404_view, custom_500_view

urlpatterns: list[URLPattern | URLResolver] = [
    path("", include("presentation.pages.urls")),
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
    path("candidate/", include("presentation.candidate.urls")),
    path("ingestion/", include("presentation.ingestion.urls")),
]

handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

if settings.DEBUG:
    urlpatterns += [
        path("403/", custom_403_view, name="error-403"),
        path("404/", custom_404_view, name="error-404"),
        path("500/", custom_500_view, name="error-500"),
    ]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [*urlpatterns] + debug_toolbar_urls()
