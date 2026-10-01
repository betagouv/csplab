from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from infrastructure.django_apps.commons.admin import stat_snapshot_list_view
from presentation.api import urls as api_urls
from presentation.ats import urls as ats_urls
from presentation.candidate import urls as candidate_urls
from presentation.identite import urls as identite_urls
from presentation.identite.admin_site import (
    LoggedAdminSite,
    LoggedOTPAdminSite,
)
from presentation.ingestion import urls as ingestion_urls
from presentation.ingestion import urls_fake_ts as ingestion_fake_ts_urls
from presentation.pages import urls as pages_urls
from presentation.pages.views import security_txt
from presentation.recruteur import urls as recruteur_urls

admin.site.__class__ = (
    LoggedOTPAdminSite if settings.ADMIN_OTP_REQUIRED else LoggedAdminSite
)

urlpatterns: list[URLPattern | URLResolver] = [
    path(".well-known/security.txt", security_txt),
    path("", include(pages_urls)),
    path("api/", include(api_urls)),
    path(
        "cockpit/stat-snapshots/",
        admin.site.admin_view(stat_snapshot_list_view),
        name="admin_stat_snapshot_list",
    ),
    path("cockpit/", admin.site.urls),
    path("candidate/", include(candidate_urls)),
    path("api/v1/", include(ingestion_urls)),
    path("api/fake-ts/", include(ingestion_fake_ts_urls)),
    path("ats/", include(ats_urls)),
    path("utilisateur/", include(identite_urls)),
    path("recruteur/", include(recruteur_urls)),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]

if settings.DEBUG and "django_browser_reload" in settings.INSTALLED_APPS:
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))
