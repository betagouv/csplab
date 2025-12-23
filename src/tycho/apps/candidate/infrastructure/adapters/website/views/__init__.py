"""Views for candidate website."""

from apps.candidate.infrastructure.adapters.website.views.home import HomeView
from apps.candidate.infrastructure.adapters.website.views.search import CorpsSearchView

__all__ = [
    "HomeView",
    "CorpsSearchView",
]
