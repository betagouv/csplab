from django.conf import settings
from django.http import HttpRequest


def matomo(request: HttpRequest) -> dict[str, object]:
    return {
        "MATOMO_BASE_URL": settings.MATOMO_BASE_URL,
        "MATOMO_SITE_ID": settings.MATOMO_SITE_ID,
    }
