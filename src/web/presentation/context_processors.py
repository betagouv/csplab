from typing import Any

from django.conf import settings
from django.http import HttpRequest


def matomo(request: HttpRequest) -> dict[str, object]:
    return {
        "MATOMO_BASE_URL": settings.MATOMO_BASE_URL,
        "MATOMO_SITE_ID": settings.MATOMO_SITE_ID,
    }


def robots(request: HttpRequest) -> dict[str, object]:
    return {"ROBOTS_INDEXING": settings.ROBOTS_INDEXING}


def skiplinks(request: HttpRequest) -> dict[str, Any]:
    return {
        "skiplinks": [
            {"link": "#content", "label": "Contenu"},
            {"link": "#footer", "label": "Pied de page"},
        ]
    }
